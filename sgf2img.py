from sgf2img import GetAllThemes, GameImageGenerator
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('sgf_name', action='store', nargs='?', help='sgf file name')
    parser.add_argument('image_name', action='store', nargs='?', help='output image file name')
    parser.add_argument('--img_size', action='store', type=int, default=1024, nargs='?', help='set the image size')
    parser.add_argument('--start_number', action='store', type=int, nargs='?')
    parser.add_argument('--start', action='store', type=int, nargs='?')
    parser.add_argument('--end', action='store', type=int, nargs='?')
    parser.add_argument('--theme', action='store', default='real-stones', help='default theme is real-stones')
    parser.add_argument('--disable_coordinates', action='store_true', default=False)
    parser.add_argument('--list_themes', action='store_true', default=False, help='list all available themes')
    parser.add_argument('--part_rect', action='store', nargs='?', help='[left,top,right,bottom] left/bottom is the origin')
    args = parser.parse_args()

    themes = GetAllThemes()
    if args.list_themes:
        print('Available thems:')
        for theme in themes.keys():
            print('\t', theme)
    elif args.sgf_name is None or args.image_name is None:
        parser.print_help()
    else:
        theme = themes[args.theme]
        part_rect = args.part_rect
        if part_rect is not None:
            part_rect = [int(x) for x in part_rect.split(',')]
        gig = GameImageGenerator(theme, not args.disable_coordinates)
        gig.get_game_image(args.sgf_name,
                           args.img_size,
                           args.start_number,
                           args.start,
                           args.end,
                           part_rect=part_rect).save(args.image_name)
