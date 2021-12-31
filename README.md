# usage:
```
usage: sgf2img.py [-h] [--start_number [START_NUMBER]] [--start [START]]
                  [--end [END]] [--theme THEME] [--list_themes]
                  [sgf_name] [image_name]

positional arguments:
  sgf_name              sgf file name
  image_name            output image file name

optional arguments:
  -h, --help            show this help message and exit
  --start_number [START_NUMBER]
  --start [START]
  --end [END]
  --theme THEME         default theme is real-stones
  --list_themes
```

# examples:

`sgf2img.py AlphaGo_AlphaGo_第一局_简体.sgf 1.jpg`

![](gallery/real-stones.jpg)

`sgf2img.py AlphaGo_AlphaGo_第一局_简体.sgf koast.jpg --theme koast --start_number 1`
![](gallery/koast.jpg)

` sgf2img.py AlphaGo_AlphaGo_第一局_简体.sgf Lizzie-look.jpg --theme Lizzie-look --start 5 --end 10`
![](gallery/Lizzie-look.jpg)