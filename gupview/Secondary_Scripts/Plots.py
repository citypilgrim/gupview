#########
#Imports#
#########

# Graph Plotting
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure

# Image process
import cv2
import numpy as np
import PIL

from .Masks import boxMask_func, lineMask_func

###########
#Operation#
###########

class Plots:
    def __init__(self, plotsize, cropsize):

        figsize = int(plotsize/80)
        self.halfcropsize = int(cropsize/2)

        # image to be processed
        self.img = None

        #intialising figure; 2D slice plot
        self.fig = Figure(figsize=(figsize, figsize), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_ylim([-5,260])

        self.X = np.linspace(-self.halfcropsize, self.halfcropsize, self.halfcropsize*2)
        self.hor = np.zeros_like(self.X)
        self.ver = np.zeros_like(self.X)

        self.hor_plot = self.ax.plot(self.X, self.hor)
        self.ver_plot = self.ax.plot(self.X, self.ver)



    def get_plot(self, image, cropLoc, cropsize, linePos, cropcanvassize):
        self.halfcropsize = int(cropsize/2)

        # Obtaining crop image
        ## Cropping image
        cropImage = image[cropLoc[1]-self.halfcropsize : cropLoc[1]+self.halfcropsize,
                          cropLoc[0]-self.halfcropsize : cropLoc[0]+self.halfcropsize]
        ## Color mapped image
        disp_ara = cv2.applyColorMap(255 - cropImage, cv2.COLORMAP_JET)
        disp_img = PIL.Image.fromarray(disp_ara)
        disp_img = disp_img.resize((cropcanvassize, cropcanvassize), PIL.Image.NEAREST)
        ## adding line mask to image
        disp_img = lineMask_func(disp_img, linePos)


        # Updating plot
        self.X = np.linspace(-self.halfcropsize,self.halfcropsize, self.halfcropsize*2)

        self.hor_plot[0].remove()
        hor_ara = cropImage[int(linePos[1] * len(cropImage))]
        self.hor_plot = self.ax.plot(self.X, hor_ara, 'C0')

        self.ver_plot[0].remove()
        ver_ara = cropImage.transpose()[int(linePos[0] * len(cropImage))]
        self.ver_plot = self.ax.plot(self.X, ver_ara, 'C1')

        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

        return disp_img


    def get_feed(self, array, cropLoc, cropsize, width, height):

        self.halfcropsize = int(cropsize/2)

        image = PIL.Image.fromarray(array)
        # Obtaining Feed Image
        feed_image = boxMask_func(image, cropLoc, cropsize)
        feed_image = feed_image.resize((width, height), PIL.Image.NEAREST)

        return feed_image
