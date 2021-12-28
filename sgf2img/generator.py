#! /usr/bin/env python3
# coding=utf-8
from re import S
from PIL import Image, ImageDraw, ImageFont
from collections import namedtuple
import random
from sgfmill import sgf, sgf_moves

Point = namedtuple('Point', ['x', 'y'])


class GridPosition:
    def __init__(self, width, size):
        self._board_width = width * 0.85
        x0 = (width - self._board_width) / 2
        y0 = (width - self._board_width) / 2
        self._grid_size = self._board_width / (size - 1)

        self._grid_pos = []
        for y in range(size):
            row_pos = []
            y_pos = int(y0 + self._grid_size * y)
            for x in range(size):
                row_pos.append(Point(int(x0 + self._grid_size * x), y_pos))
            self._grid_pos.append(row_pos)

        self._grid_pos = self._grid_pos[::-1]

        self._star_coords = self.__get_star_point_coords(size)

    def __get_star_point_coords(self, size):
        if size < 7:
            return []
        elif size <= 11:
            star_point_pos = 3
        else:
            star_point_pos = 4

        return [star_point_pos - 1, size - star_point_pos] + (
            [int(size / 2)] if size % 2 == 1 and size > 7 else []
        )

    @property
    def star_coords(self):
        return self._star_coords

    @property
    def grid_size(self):
        return self._grid_size

    @property
    def board_width(self):
        return self._board_width

    @property
    def x0(self):
        return self._grid_pos[0][0].x

    @property
    def y0(self):
        return self._grid_pos[0][0].y

    @property
    def x1(self):
        return self._grid_pos[-1][-1].x

    @property
    def y1(self):
        return self._grid_pos[-1][-1].y

    def __getitem__(self, index):
        return self._grid_pos[index]


class GameImageGenerator:
    def __init__(self, theme, with_coordinates=True):
        self.theme = theme
        self.with_coordinates = with_coordinates
        self.size = None
        self.default_width = 1024
        self._board_image = None
        self._grid_pos = None
        self._black_images = None
        self._white_images = None
        self.font = ImageFont.truetype('DroidSansMono.ttf', int(self.default_width * 0.02))

    def get_board_image(self, size=19):
        if self.size == size and self._board_imgage is not None:
            return self._board_image

        self.size = size
        img = Image.open(self.theme['board'])
        w, h = img.size
        if self.theme['board_resize']:
            self._board_image = img.resize((self.default_width, self.default_width)).convert('RGB')
        else:
            self._board_image = Image.new('RGB', (self.default_width, self.default_width))
            for x in range(0, self.default_width, w):
                for y in range(0, self.default_width, h):
                    self._board_image.paste(img, (x, y))

        draw = ImageDraw.ImageDraw(self._board_image)
        grid_pos = self.get_grid_pos(size)
        for i in range(size):
            draw.line((grid_pos[i][0].x, grid_pos[i][0].y, grid_pos[i][-1].x, grid_pos[i][0].y), self.theme['line_color'])
            draw.line((grid_pos[0][i].x, grid_pos[0][i].y, grid_pos[-1][i].x, grid_pos[-1][i].y), fill=self.theme['line_color'])

        start_size = self.default_width * 0.005
        for x in grid_pos.star_coords:
            for y in grid_pos.star_coords:
                _x, _y = grid_pos[y][x]
                draw.ellipse((_x - start_size,
                              _y - start_size,
                              _x + start_size,
                              _y + start_size),
                             fill=self.theme['line_color'])

        grid_size = grid_pos.grid_size
        if self.with_coordinates:
            fw, fh = self.font.getsize('A')
            for i in range(size):
                draw.text((grid_pos[0][i].x, grid_pos[0][i].y + grid_size),
                          chr(ord('A') + i),
                          fill=self.theme['line_color'],
                          font=self.font,
                          anchor='mm')
                draw.text((grid_pos[-1][i].x, grid_pos[-1][i].y - grid_size),
                          chr(ord('A') + i),
                          fill=self.theme['line_color'],
                          font=self.font,
                          anchor='mm')
                draw.text((grid_pos[i][0].x - grid_size - fw, grid_pos[i][0].y),
                          str(i + 1),
                          fill=self.theme['line_color'],
                          font=self.font,
                          anchor='mm')
                draw.text((grid_pos[i][-1].x + grid_size, grid_pos[i][-1].y),
                          str(i + 1),
                          fill=self.theme['line_color'],
                          font=self.font,
                          anchor='mm')

        return self._board_image

    def get_grid_pos(self, size=19):
        if size != size or self._grid_pos is None:
            self._grid_pos = GridPosition(self.default_width, size)
        return self._grid_pos

    def get_stone_image(self, s):
        if s is None:
            return None
        images = self._black_images if s == 'b' else self._white_images
        return images[random.randint(0, len(images) - 1)]
        # if number:
        #     number = str(number)
        #     draw = ImageDraw.ImageDraw(stone)
        #     w, h = stone.size
        #     _w, _h = self.font.getsize(number)
        #     draw.text(((w - _w) // 2, (h - _h) // 2),
        #               number,
        #               fill='black' if s == 'w' else 'white',
        #               font=self.font)
        # return stone

    def load_stone_images(self, force=False):
        if force or self._black_images is None:
            stone_size = int(self.get_grid_pos().grid_size * 0.9)
            self._black_images = [Image.open(b).resize((stone_size, stone_size)) for b in self.theme['black']]
            self._white_images = [Image.open(w).resize((stone_size, stone_size)) for w in self.theme['white']]

    def get_game_image(self, sgf_path, img_size=None, start_number=None, start=None, end=None):
        try:
            sgf_game = sgf.Sgf_game.from_bytes(open(sgf_path, 'rb').read())
        except ValueError:
            raise Exception("bad sgf file")

        try:
            board, plays = sgf_moves.get_setup_and_moves(sgf_game)
        except ValueError as e:
            raise Exception(str(e))

        for i, (colour, move) in enumerate(plays, start=1):
            if move is None:
                continue

            row, col = move
            try:
                board.play(row, col, colour)
            except ValueError:
                raise Exception("illegal move in sgf file")

            if i == end:
                break

        grid_pos = self.get_grid_pos(sgf_game.get_size())
        board_image = self.get_board_image(sgf_game.get_size()).copy()
        self.load_stone_images()
        stone_offset = self._black_images[0].size[0] // 2
        self.size = sgf_game.get_size()
        # draw stones
        for x in range(self.size):
            for y in range(self.size):
                stone_image = self.get_stone_image(board.get(x, y))
                if stone_image:
                    board_image.paste(stone_image,
                                      #   (grid_pos[x][y].x - stone_offset,
                                      #    grid_pos[x][y].y - stone_offset),
                                      (grid_pos[x][y].x - stone_offset + random.randint(-2, 2),
                                       grid_pos[x][y].y - stone_offset + random.randint(-2, 2)),
                                      stone_image)

        # draw numbers
        if start:
            draw = ImageDraw.ImageDraw(board_image)
            if start_number is None:
                start_number = start

            coor = {}
            for i, (colour, move) in enumerate(plays, start=1):
                if move is None:
                    continue
                if i >= start:
                    if move in coor:
                        coor[move].append(i)
                    else:
                        coor[move] = [i]
                        row, col = move
                        draw.text((grid_pos[row][col].x, grid_pos[row][col].y),
                                  str(start_number),
                                  fill='white' if board.get(row, col) == 'b' else 'black',
                                  font=self.font,
                                  anchor='mm')
                        start_number += 1
                if i == end:
                    break

            for counts in filter(lambda x: len(x) > 1, coor.values()):
                print(' = '.join([str(c) for c in counts]))

        if img_size:
            board_image = board_image.resize((img_size, img_size))
        return board_image
