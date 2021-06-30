from ui.theme import *

def tempColor(temp):
    color = color_white
    if temp:
        if temp < 20:
            color = color_blue
        if 27 > temp > 19:
            color = color_lakeblue
        if 30 > temp > 26:
            color = color_green
        if 35 > temp > 29:
            color = color_lightgreen
        if 40 > temp > 34:
            color = color_pink
        if 45 > temp > 39:
            color = color_orange
        if 50 > temp > 44:
            color =color_peach
        if temp > 49:
            color = color_red
    return color

def cpuUseColor(use):
    color = color_white
    if use:
        if use < 3:
            color = color_green
        if 5 > use > 2:
            color = color_lightgreen
        if 10 > use > 4:
            color = color_lakeblue
        if 20 > use > 9:
            color = color_blue
        if 50 > use > 19:
            color = color_orange
        if 80 > use > 49:
            color = color_pink
        if 90 > use > 79:
            color =color_peach
        if use > 89:
            color = color_red
    return color