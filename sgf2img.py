from sgf2img import GetAllThemes, GameImageGenerator
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('sgf_name', action='store', nargs='?', help='sgf file name')
    parser.add_argument('image_name', action='store', nargs='?', help='output image file name')
    parser.add_argument('--start', action='store', type=int, nargs='?')
    parser.add_argument('--from', action='store', type=int, nargs='?')
    parser.add_argument('--to', action='store', type=int, nargs='?')
    parser.add_argument('--theme', action='store', default='real-stones', help='default theme is real-stones')
    parser.add_argument('--list_themes', action='store_true', default=False)
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
        gig = GameImageGenerator(theme)
        gig.get_game_image(args.sgf_name, start=1).save(args.image_name)
