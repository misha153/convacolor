from math import acos, pi, sqrt
from convacolor.ncs_data import data
from functools import wraps


# ------------------------------------------
#   Module repository on GitHub -:
#   https://github.com/misha153/convacolor
# 
#   Several algorithms for converting from rgb to other color models
# 
#   Contact me if you want me to add something. My email:
#   mishakarpov153@gmail.com
# ------------------------------------------


def ParamCheckList(func):

    # For get_cmyk and get_hsv
    @wraps(func)
    def inner(r, g, b, output_mode='i'):

        if r > 255 or g > 255 or b > 255:
            raise ValueError("Values cannot be greater than 255")
        elif r < 0 or g < 0 or b < 0:
            raise ValueError("Values cannot be negative")
        
        if output_mode != 'i' and output_mode != 'f':
            raise ValueError("output_mode must be 'i' or 'f' ")
        
        return func(r, g, b, output_mode)
    
    return inner


def ParamCheckStr(func):

    # For get_hex and get_ncs
    @wraps(func)
    def inner(r, g, b):

        if r > 255 or g > 255 or b > 255:
            raise ValueError("Values cannot be greater than 255")
        elif r < 0 or g < 0 or b < 0:
            raise ValueError("Values cannot be negative")
        
        return func(r, g, b)
    
    return inner


@ParamCheckList
def get_cmyk(r: int, g: int, b: int, output_mode='i' or 'f') -> list:

    """
    This function converts from RGB color model to CMYK color model

    CMYK wiki => https://en.wikipedia.org/wiki/CMYK_color_model

    :param r: int
    :param g: int
    :param b: int
    :param output_mode: if 'f' is specified, all values will be between 0 and 1
    :return: the list of cmyk values
    """

    rgb_scale = 255
    cmyk_scale = 100

    if (r, g, b) == (0, 0, 0):
        return 0, 0, 0, cmyk_scale
    
    c = 1 - r / rgb_scale
    m = 1 - g / rgb_scale
    y = 1 - b / rgb_scale

    min_cmy = min(c, m, y)
    c = (c - min_cmy) / (1 - min_cmy)
    m = (m - min_cmy) / (1 - min_cmy)
    y = (y - min_cmy) / (1 - min_cmy)
    k = min_cmy

    cmyk = [round(c * cmyk_scale), round(m * cmyk_scale), round(y * cmyk_scale), round(k * cmyk_scale)]

    if output_mode == 'i':
        return cmyk
    else:
        c, m, y, k = cmyk
        cmyk_float = [round(c / 100, 4), round(m / 100, 4), round(y / 100, 4), round(k / 100, 4)]

        return cmyk_float


@ParamCheckList
def get_hsv(r: int, g: int, b: int, output_mode='i' or 'f') -> list:

    """
    This function converts from RGB color model to HSV color model

    HSV wiki => https://en.wikipedia.org/wiki/HSL_and_HSV

    :param r: int
    :param g: int
    :param b: int
    :param output_mode: if 'f' is specified, all values will be between 0 and 1
    :return: the list of hsv values
    """

    maxim = max(r, g, b)
    minim = min(r, g, b)
    v = round(maxim / 2.55)

    if maxim == 0:
        s = 0
    else:
        s = round(1 - minim / maxim, 2) * 100

    div = sqrt((r ** 2) + (g ** 2) + (b ** 2) - r * g - r * b - g * b) + 1

    if g >= b:
        h = round(acos((r - g / 2 - b / 2) / div) * 180 / pi)
    else:
        h = round(360 - (acos((r - g / 2 - b / 2) / div) * 180 / pi))

    hsv = [h, round(s), v]

    if output_mode == 'i':
        return [h, round(s), v]
    else:
        h, s, v = hsv
        hsv_float = [round(h / 360, 4), round(s / 100, 4), round(v / 100, 4)]

        return hsv_float


@ParamCheckStr
def get_hex(r: int, g: int, b: int) -> str:

    """
    This function converts from RGB color model to NCS (Natural Color System)

    NCS wiki => https://en.wikipedia.org/wiki/Natural_Color_System

    :param r: int
    :param g: int
    :param b: int
    :return: the hex equivalent of rgb
    """

    r, g, b = '{:X}'.format(r), '{:X}'.format(g), '{:X}'.format(b)
    res = ''

    if len(r) == 1:
        res += f'0{r}'
    else:
        res += r
    
    if len(g) == 1:
        res += f'0{g}'
    else:
        res += g

    if len(b) == 1:
        res += f'0{b}'
    else:
        res += b

    return f'#{res}'
    

@ParamCheckStr
def get_ncs(r: int, g: int, b: int) -> str:
        
        """
        This function converts from RGB to NCS (Natural Color System)

        NCS wiki => https://en.wikipedia.org/wiki/Natural_Color_System

        :param r: int
        :param g: int
        :param b: int
        :return: the ncs equivalent of rgb
        """
        
        # We use the Hue value and the Value from HSV
        # to more accurately determine the color
        v = round(max(r, g, b) / 2.55)

        div = sqrt((r ** 2) + (g ** 2) + (b ** 2) - r * g - r * b - g * b) + 1

        if g >= b:
            h = round(acos((r - g / 2 - b / 2) / div) * 180 / pi)
        else:
            h = round(360 - (acos((r - g / 2 - b / 2) / div) * 180 / pi))

        # White to black check
        blackness = round(100-v / 10) * 10

        if blackness < 5:
            blackness = 5
        if r <= 10 and g <= 10 and b <= 10:
            return 'S9000-N'
        
        dif_rg = abs(r - g)
        dif_rb = abs(r - b)
        dif_gb = abs(g - b)

        if dif_rg <= 5 and dif_rb <= 5 and dif_gb <= 5:

            str_blackness = str(blackness)

            if len(str_blackness) == 1:
                return f'S0{str_blackness}00-N'
            else:
                return f'S{str_blackness}00-N'
        
        color_range: str
        len_is: int

        # Hue definition
        if h > 348 or h < 47:
            len_is = 10
            color_range = 'R'  # relative to yellow
        elif 47 <= h <= 53:
            len_is = 7
            color_range = 'Y'  # is single-yellow
        elif h < 157:
            len_is = 10
            color_range = 'Y'  # relative to green
        elif 157 <= h <= 163:
            len_is = 7
            color_range = 'G'  # is single-green
        elif h < 194:
            len_is = 10
            color_range = 'G'  # relative to blue
        elif 194 <= h <= 200:
            len_is = 7
            color_range = 'B'  # is single-blue
        elif h < 342:
            len_is = 10
            color_range = 'B'  # relative to red
        elif 342 <= h <= 348:
            len_is = 7
            color_range = 'R'  # is single-red

        count_ncs = 0
        count_rgb = 1
        dif_list: list = []
        ncs_list: list = []

        for i in range(0, 1302):

            ncs = data[count_ncs]  # string
            rgb = data[count_rgb]  # list

            if ncs[-1] == color_range and len(ncs) == len_is:
                dif_list.append(abs(rgb[0] - r) + abs(rgb[1] - g) + abs(rgb[2] - b))
                ncs_list.append(ncs)

            count_ncs += 2
            count_rgb += 2

        return ncs_list[dif_list.index(min(dif_list))]
