#########
#Imports#
#########

import os
from PIL import ImageDraw
import numpy as np


###########
#Functions#
###########

def draw_rectangle(draw, coordinates, outline, width):
    for i in range(width):
        rect_start = (coordinates[0][1] - i, coordinates[0][0] - i)
        rect_end = (coordinates[1][1] + i, coordinates[1][0] + i)
        draw.rectangle((rect_start, rect_end), outline = outline)

def boxMask_func(image, cropLoc, cropsize):
    halfcropsize = int(cropsize/2)
    x, y = cropLoc

    draw = ImageDraw.Draw(image)
    transparent_area = ((y-halfcropsize, x-halfcropsize), (y+halfcropsize, x+halfcropsize))

    draw_rectangle(draw, transparent_area, outline=255, width=3)

    return image

def rectMask_func(image, cropLoc, cropdimension):
    halfcropsize_x, halfcropsize_y = int(cropdimension[0]/2), int(cropdimension[1]/2)
    x, y = cropLoc

    draw = ImageDraw.Draw(image)
    transparent_area = ((y-halfcropsize_y, x-halfcropsize_x), (y+halfcropsize_y, x+halfcropsize_x))

    draw_rectangle(draw, transparent_area, outline=255, width=3)

    return image

def lineMask_func(image, linePos):
    array = np.asarray(image)
    xPos = int(linePos[0] * len(array))
    yPos = int(linePos[1] * len(array))

    draw = ImageDraw.Draw(image)

    horLine_coords = [(0, yPos), (len(array), yPos)]
    draw.line(horLine_coords, fill=(255, 255, 255), width = 1)

    verLine_coords = [(xPos, 0), (xPos, len(array))]
    draw.line(verLine_coords, fill=(255, 255, 255), width = 1)

    return image