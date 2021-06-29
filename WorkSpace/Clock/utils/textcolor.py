from ui.theme import *

def tempColor(temp):
    color = color_white
    if temp:
        if temp < 20:
            color = color_green
        if 27 > temp > 19:
            color = color_lightgreen
        if 30 > temp > 26:
            color = color_lakeblue
        if 35 > temp > 29:
            color = color_blue
        if 40 > temp > 34:
            color = color_pink
        if 45 > temp > 39:
            color = color_peach
        if 50 > temp > 44:
            color = color_red
        if temp > 49:
            color = color_purple
    return color