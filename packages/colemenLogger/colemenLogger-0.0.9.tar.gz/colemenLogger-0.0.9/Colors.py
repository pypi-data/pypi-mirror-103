# import fileUtils
# import RaLog.fileUtils as fileUtils
import cssutils
import re
import math
from pprint import pprint


class Colors:
    def __init__(self):
        self.data = {}
        self.__setDefaults()

    def __setDefaults(self):
        self.data['colors'] = {
            "lavender": {"hex": "#E6E6FA", "rgb": [230, 230, 250]},
            "thistle": {"hex": "#D8BFD8", "rgb": [216, 191, 216]},
            "plum": {"hex": "#DDA0DD", "rgb": [221, 160, 221]},
            "violet": {"hex": "#EE82EE", "rgb": [238, 130, 238]},
            "orchid": {"hex": "#DA70D6", "rgb": [218, 112, 214]},
            "fuchsia": {"hex": "#FF00FF", "rgb": [255, 0, 255]},
            "magenta": {"hex": "#FF00FF", "rgb": [255, 0, 255]},
            "mediumorchid": {"hex": "#BA55D3", "rgb": [186, 85, 211]},
            "mediumpurple": {"hex": "#9370DB", "rgb": [147, 112, 219]},
            "blueviolet": {"hex": "#8A2BE2", "rgb": [138, 43, 226]},
            "dark_violet": {"hex": "#9400D3", "rgb": [148, 0, 211]},
            "dark_orchid": {"hex": "#9932CC", "rgb": [153, 50, 204]},
            "dark_magenta": {"hex": "#8B008B", "rgb": [139, 0, 139]},
            "purple": {"hex": "#800080", "rgb": [128, 0, 128]},
            "indigo": {"hex": "#4B0082", "rgb": [75, 0, 130]},
            "powderblue": {"hex": "#B0E0E6", "rgb": [176, 224, 230]},
            "light_blue": {"hex": "#ADD8E6", "rgb": [173, 216, 230]},
            "light_skyblue": {"hex": "#87CEFA", "rgb": [135, 206, 250]},
            "skyblue": {"hex": "#87CEEB", "rgb": [135, 206, 235]},
            "deepskyblue": {"hex": "#00BFFF", "rgb": [0, 191, 255]},
            "light_steelblue": {"hex": "#B0C4DE", "rgb": [176, 196, 222]},
            "dodgerblue": {"hex": "#1E90FF", "rgb": [30, 144, 255]},
            "cornflowerblue": {"hex": "#6495ED", "rgb": [100, 149, 237]},
            "steelblue": {"hex": "#4682B4", "rgb": [70, 130, 180]},
            "royalblue": {"hex": "#4169E1", "rgb": [65, 105, 225]},
            "blue": {"hex": "#0000FF", "rgb": [0, 0, 255]},
            "mediumblue": {"hex": "#0000CD", "rgb": [0, 0, 205]},
            "dark_blue": {"hex": "#00008B", "rgb": [0, 0, 139]},
            "navy": {"hex": "#000080", "rgb": [0, 0, 128]},
            "midnightblue": {"hex": "#191970", "rgb": [25, 25, 112]},
            "mediumslateblue": {"hex": "#7B68EE", "rgb": [123, 104, 238]},
            "slateblue": {"hex": "#6A5ACD", "rgb": [106, 90, 205]},
            "dark_slateblue": {"hex": "#483D8B", "rgb": [72, 61, 139]},
            "light_cyan": {"hex": "#E0FFFF", "rgb": [224, 255, 255]},
            "cyan": {"hex": "#00FFFF", "rgb": [0, 255, 255]},
            "aqua": {"hex": "#00FFFF", "rgb": [0, 255, 255]},
            "aquamarine": {"hex": "#7FFFD4", "rgb": [127, 255, 212]},
            "mediumaquamarine": {"hex": "#66CDAA", "rgb": [102, 205, 170]},
            "paleturquoise": {"hex": "#AFEEEE", "rgb": [175, 238, 238]},
            "turquoise": {"hex": "#40E0D0", "rgb": [64, 224, 208]},
            "mediumturquoise": {"hex": "#48D1CC", "rgb": [72, 209, 204]},
            "dark_turquoise": {"hex": "#00CED1", "rgb": [0, 206, 209]},
            "light_seagreen": {"hex": "#20B2AA", "rgb": [32, 178, 170]},
            "cadetblue": {"hex": "#5F9EA0", "rgb": [95, 158, 160]},
            "dark_cyan": {"hex": "#008B8B", "rgb": [0, 139, 139]},
            "teal": {"hex": "#008080", "rgb": [0, 128, 128]},
            "lawngreen": {"hex": "#7CFC00", "rgb": [124, 252, 0]},
            "chartreuse": {"hex": "#7FFF00", "rgb": [127, 255, 0]},
            "limegreen": {"hex": "#32CD32", "rgb": [50, 205, 50]},
            "lime": {"hex": "#00FF00", "rgb": [0, 255, 0]},
            "forestgreen": {"hex": "#228B22", "rgb": [34, 139, 34]},
            "green": {"hex": "#008000", "rgb": [0, 128, 0]},
            "dark_green": {"hex": "#006400", "rgb": [0, 100, 0]},
            "greenyellow": {"hex": "#ADFF2F", "rgb": [173, 255, 47]},
            "yellowgreen": {"hex": "#9ACD32", "rgb": [154, 205, 50]},
            "springgreen": {"hex": "#00FF7F", "rgb": [0, 255, 127]},
            "mediumspringgreen": {"hex": "#00FA9A", "rgb": [0, 250, 154]},
            "light_green": {"hex": "#90EE90", "rgb": [144, 238, 144]},
            "palegreen": {"hex": "#98FB98", "rgb": [152, 251, 152]},
            "dark_seagreen": {"hex": "#8FBC8F", "rgb": [143, 188, 143]},
            "mediumseagreen": {"hex": "#3CB371", "rgb": [60, 179, 113]},
            "seagreen": {"hex": "#2E8B57", "rgb": [46, 139, 87]},
            "olive": {"hex": "#808000", "rgb": [128, 128, 0]},
            "dark_olivegreen": {"hex": "#556B2F", "rgb": [85, 107, 47]},
            "olivedrab": {"hex": "#6B8E23", "rgb": [107, 142, 35]},
            "light_yellow": {"hex": "#FFFFE0", "rgb": [255, 255, 224]},
            "lemonchiffon": {"hex": "#FFFACD", "rgb": [255, 250, 205]},
            "light_goldenrodyellow": {"hex": "#FAFAD2", "rgb": [250, 250, 210]},
            "papayawhip": {"hex": "#FFEFD5", "rgb": [255, 239, 213]},
            "moccasin": {"hex": "#FFE4B5", "rgb": [255, 228, 181]},
            "peachpuff": {"hex": "#FFDAB9", "rgb": [255, 218, 185]},
            "palegoldenrod": {"hex": "#EEE8AA", "rgb": [238, 232, 170]},
            "khaki": {"hex": "#F0E68C", "rgb": [240, 230, 140]},
            "dark_khaki": {"hex": "#BDB76B", "rgb": [189, 183, 107]},
            "yellow": {"hex": "#FFFF00", "rgb": [255, 255, 0]},
            "coral": {"hex": "#FF7F50", "rgb": [255, 127, 80]},
            "tomato": {"hex": "#FF6347", "rgb": [255, 99, 71]},
            "orangered": {"hex": "#FF4500", "rgb": [255, 69, 0]},
            "gold": {"hex": "#FFD700", "rgb": [255, 215, 0]},
            "orange": {"hex": "#FFA500", "rgb": [255, 165, 0]},
            "dark_orange": {"hex": "#FF8C00", "rgb": [255, 140, 0]},
            "light_salmon": {"hex": "#FFA07A", "rgb": [255, 160, 122]},
            "salmon": {"hex": "#FA8072", "rgb": [250, 128, 114]},
            "dark_salmon": {"hex": "#E9967A", "rgb": [233, 150, 122]},
            "light_coral": {"hex": "#F08080", "rgb": [240, 128, 128]},
            "indianred": {"hex": "#CD5C5C", "rgb": [205, 92, 92]},
            "crimson": {"hex": "#DC143C", "rgb": [220, 20, 60]},
            "firebrick": {"hex": "#B22222", "rgb": [178, 34, 34]},
            "red": {"hex": "#FF0000", "rgb": [255, 0, 0]},
            "dark_red": {"hex": "#8B0000", "rgb": [139, 0, 0]},
            "pink": {"hex": "#FFC0CB", "rgb": [255, 192, 203]},
            "light_pink": {"hex": "#FFB6C1", "rgb": [255, 182, 193]},
            "hotpink": {"hex": "#FF69B4", "rgb": [255, 105, 180]},
            "deeppink": {"hex": "#FF1493", "rgb": [255, 20, 147]},
            "palevioletred": {"hex": "#DB7093", "rgb": [219, 112, 147]},
            "mediumvioletred": {"hex": "#C71585", "rgb": [199, 21, 133]},
            "white": {"hex": "#FFFFFF", "rgb": [255, 255, 255]},
            "snow": {"hex": "#FFFAFA", "rgb": [255, 250, 250]},
            "honeydew": {"hex": "#F0FFF0", "rgb": [240, 255, 240]},
            "mintcream": {"hex": "#F5FFFA", "rgb": [245, 255, 250]},
            "azure": {"hex": "#F0FFFF", "rgb": [240, 255, 255]},
            "aliceblue": {"hex": "#F0F8FF", "rgb": [240, 248, 255]},
            "ghostwhite": {"hex": "#F8F8FF", "rgb": [248, 248, 255]},
            "whitesmoke": {"hex": "#F5F5F5", "rgb": [245, 245, 245]},
            "seashell": {"hex": "#FFF5EE", "rgb": [255, 245, 238]},
            "beige": {"hex": "#F5F5DC", "rgb": [245, 245, 220]},
            "oldlace": {"hex": "#FDF5E6", "rgb": [253, 245, 230]},
            "floralwhite": {"hex": "#FFFAF0", "rgb": [255, 250, 240]},
            "ivory": {"hex": "#FFFFF0", "rgb": [255, 255, 240]},
            "antiquewhite": {"hex": "#FAEBD7", "rgb": [250, 235, 215]},
            "linen": {"hex": "#FAF0E6", "rgb": [250, 240, 230]},
            "lavenderblush": {"hex": "#FFF0F5", "rgb": [255, 240, 245]},
            "mistyrose": {"hex": "#FFE4E1", "rgb": [255, 228, 225]},
            "gainsboro": {"hex": "#DCDCDC", "rgb": [220, 220, 220]},
            "light_gray": {"hex": "#D3D3D3", "rgb": [211, 211, 211]},
            "silver": {"hex": "#C0C0C0", "rgb": [192, 192, 192]},
            "dark_gray": {"hex": "#A9A9A9", "rgb": [169, 169, 169]},
            "gray": {"hex": "#808080", "rgb": [128, 128, 128]},
            "dimgray": {"hex": "#696969", "rgb": [105, 105, 105]},
            "light_slategray": {"hex": "#778899", "rgb": [119, 136, 153]},
            "slategray": {"hex": "#708090", "rgb": [112, 128, 144]},
            "dark_slategray": {"hex": "#2F4F4F", "rgb": [47, 79, 79]},
            "black": {"hex": "#000000", "rgb": [0, 0, 0]},
            "cornsilk": {"hex": "#FFF8DC", "rgb": [255, 248, 220]},
            "blanchedalmond": {"hex": "#FFEBCD", "rgb": [255, 235, 205]},
            "bisque": {"hex": "#FFE4C4", "rgb": [255, 228, 196]},
            "navajowhite": {"hex": "#FFDEAD", "rgb": [255, 222, 173]},
            "wheat": {"hex": "#F5DEB3", "rgb": [245, 222, 179]},
            "burlywood": {"hex": "#DEB887", "rgb": [222, 184, 135]},
            "tan": {"hex": "#D2B48C", "rgb": [210, 180, 140]},
            "rosybrown": {"hex": "#BC8F8F", "rgb": [188, 143, 143]},
            "sandybrown": {"hex": "#F4A460", "rgb": [244, 164, 96]},
            "goldenrod": {"hex": "#DAA520", "rgb": [218, 165, 32]},
            "peru": {"hex": "#CD853F", "rgb": [205, 133, 63]},
            "chocolate": {"hex": "#D2691E", "rgb": [210, 105, 30]},
            "saddlebrown": {"hex": "#8B4513", "rgb": [139, 69, 19]},
            "sienna": {"hex": "#A0522D", "rgb": [160, 82, 45]},
            "brown": {"hex": "#A52A2A", "rgb": [165, 42, 42]},
            "maroon": {"hex": "#800000", "rgb": [128, 0, 0]}
        }

        self.data['indentGradientColors'] = [
            f"\033[38;2;205;92;92m",
            f"\033[38;2;240;128;128m",
            f"\033[38;2;250;128;114m",
            f"\033[38;2;233;150;122m",
            f"\033[38;2;255;160;122m"
        ]

    def __findColorByName(self, name):
        if name in self.data['colors']:
            return self.data['colors'][name]
        return False

    def getRGBByColorName(self, name):
        name = name.strip()
        name = name.lower()
        # print(f"getRGBByColorName: {name}")
        colorData = self.__findColorByName(name)
        if colorData is not False:
            return colorData['rgb']
        else:
            return False

    def genRGBTextColorSeq(self, rgb):
        return f"\033[38;2;{rgb[0]};{rgb[1]};{rgb[2]}m"

    def genRGBBgColorSeq(self, rgb=False):
        if rgb is False:
            return ""
        return f"\033[48;2;{rgb[0]};{rgb[1]};{rgb[2]}m"

    def getRGB(self, value):
        rgb = False
        if self.__isHexValue(value) is True:
            rgb = self.__hexToRGB(value)
        else:
            rgb = self.getRGBByColorName(value)
        return rgb

    def getSeq(self, value, sType="TEXT"):
        rgb = self.getRGB(value)
        if rgb is not False:
            if sType == "TEXT":
                return self.genRGBTextColorSeq(rgb)
            if sType == "BG":
                return self.genRGBBgColorSeq(rgb)
        return False

    def __isHexValue(self, string):
        match = re.search(r'\#[a-zA-Z0-9]{6}', string)
        if match is not None:
            return True
        return False

    def __hexToRGB(self, hexValue):
        h = hexValue.lstrip("#")
        rgb = None
        try:
            rgb = tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
            return rgb
        except ValueError:
            print(f"Invalid Hex Value Provided: {hexValue}")
            return None
        return rgb

    def RGBToHex(self, color):
        r, g, b = color
        return "#{0:02x}{1:02x}{2:02x}".format(self.clamp(r), self.clamp(g), self.clamp(b))

    def clamp(self, x):
        return max(0, min(x, 255))

    def rgbArrayToTextSeq(self, array):
        output = []
        for x in array:
            output.append(self.genRGBBgColorSeq(x))
        return output

    def calculateGradient(self, c1, c2, steps=50):
        output = []

        r1, g1, b1 = self.getRGB(c1)
        r2, g2, b2 = self.getRGB(c2)
        rdelta, gdelta, bdelta = (r2-r1)/steps, (g2-g1)/steps, (b2-b1)/steps
        # pylint: disable = unused-variable
        for step in range(steps):
            r1 += math.ceil(rdelta)
            g1 += math.ceil(gdelta)
            b1 += math.ceil(bdelta)
            hexStr = self.RGBToHex([r1, g1, b1])
            output.append(hexStr)
        return output
