#########
#Imports#
#########

# Python Basics
from decimal import Decimal

# Graph Plotting
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure

# Image process
import numpy as np
import PIL
from .Masks import rectMask_func

# Parameters
import Parameters as para


###########
#Operation#
###########

class Flouro:
    def __init__(self, plotsize, cropsize):

        figsize = int(plotsize/80)
        self.halfcropsize = int(cropsize/2)

        # image to be processed
        self.img = None

        self.count = 0

        #intialising figure
        self.fig = Figure(figsize=(figsize, figsize), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_ylim(para.ylim)
        self.ax.set_xlim([self.count-para.xlim,self.count])

        self.count_ara = np.array([])
        self.flour_ara = np.array([])
        self.flour_plot = self.ax.plot(self.count_ara, self.flour_ara)


    def get_plot(self, image, cropLoc, cropdimension, xlim, flourSum_res):
        halfcropsize_x, halfcropsize_y = int(cropdimension[0] / 2), int(cropdimension[1] / 2)

        # Obtaining crop image
        cropImage = image[cropLoc[1]-halfcropsize_y : cropLoc[1]+halfcropsize_y,
                          cropLoc[0]-halfcropsize_x : cropLoc[0]+halfcropsize_x]
        flour = np.sum(cropImage)

        # appending new values
        self.count_ara = np.append(self.count_ara, self.count)
        self.count += 1
        self.flour_ara = np.append(self.flour_ara, flour)

        # deleting beyond the limit
        if len(self.count_ara) > xlim:
            self.count_ara = self.count_ara[-xlim:]
            self.flour_ara = self.flour_ara[-xlim:]
        self.flour_plot[0].remove()

        # updating plot
        self.flour_plot = self.ax.plot(self.count_ara, self.flour_ara, 'o', color='C0')
        self.ax.set_xlim([self.count-xlim,self.count])
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

        # updating display number
        flourSum_res.configure(text='%.5E' % Decimal(str(flour)))

    def get_feed(self, array, cropLoc, cropdimension, width, height):

        image = PIL.Image.fromarray(array)
        # Obtaining Feed Image
        feed_image = rectMask_func(image, cropLoc, cropdimension)
        feed_image = feed_image.resize((width, height), PIL.Image.NEAREST)

        return feed_image
