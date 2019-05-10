#########
#Imports#
#########

# Python Basics
import sys
import os
import ast
from threading import Thread
import time

# Interfacing
if sys.version_info[0] == 3:    # for Python3
    import tkinter as tk
else:    # for Python2
    import Tkinter as tk

# Image process
import PIL.Image, PIL.ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Secondary Script
from Secondary_Scripts.VideoCapture import VideoCapture
# from Secondary_Scripts.VideoCapture_old import VideoCapture # for testing
from Secondary_Scripts.Plots import Plots

# Initialisation Parameters
import Parameters as para


###########
#Operation#
###########

class App:
    def __init__(self, window_title):

        self.window = tk.Tk()
        self.window.wm_title(window_title)

        # open video source (by default this will try to open the computer webcam)
        self.vid = VideoCapture()

        # initilaise slice plot
        self.plotsize = para.plotsize
        self.cropcanvassize = para.cropcanvassize
        self.cropsize = para.cropsize # box crop of length, each pixel is 3.75um
        self.plot = Plots(self.plotsize, self.cropsize)

        # File saving setting
        self.save_dir = para.save_dir # the saving directory has to first be created already
        def dir_update(event):
            self.save_dir = dir_entry.get()
            dir_res.configure(text='dir = ' + self.save_dir)
        tk.Label(self.window, text='Save Directory', font='Helvetica 12 bold').grid(row=0, column=0)
        dir_entry = tk.Entry(self.window, textvariable=tk.StringVar(self.window, value=self.save_dir))
        dir_entry.bind("<Return>", dir_update)
        dir_entry.grid(row=1, column=0)
        dir_res = tk.Label(self.window, text='dir = ' + self.save_dir)
        dir_res.grid(row=2, column=0)

        def file_update(event):
            frame = self.vid.get_frame()
            save_filename = file_entry.get()
            save_name = self.save_dir + save_filename
            frame_image = PIL.Image.fromarray(frame)
            frame_image.save(os.path.join(self.save_dir, save_filename))
            file_res.configure(text='file saved at: ' + save_name)
            file_entry.delete(0, tk.END)
            file_entry.insert(0, '.bmp')
        tk.Label(self.window, text='Save Filename', font='Helvetica 12 bold').grid(row=3, column=0)
        file_entry = tk.Entry(self.window, textvariable=tk.StringVar(self.window, value='.bmp'))
        file_entry.bind("<Return>", file_update)
        file_entry.grid(row=4, column=0)
        file_res = tk.Label(self.window, text='file not saved')
        file_res.grid(row=5, column=0)

        # Exposure Time setting
        def evaluate(event):
            ExposureTime = eval(entry.get())
            self.vid.c0.ExposureTime = ExposureTime
            exposure_res.configure(text='Exposure Time [us] = ' + str(eval(entry.get())))
        tk.Label(self.window, text="Limit=39 to 6.71089e+07").grid(row=2, column=1)
        entry = tk.Entry(self.window, textvariable=tk.StringVar(self.window, value=str(self.vid.c0.ExposureTime)))
        entry.bind("<Return>", evaluate)
        entry.grid(row=1, column=1)
        exposure_res = tk.Label(self.window, text='Exposure Time [us] = ' + str(self.vid.c0.ExposureTime), font='Helvetica 12 bold')
        exposure_res.grid(row=0, column=1)

        # crop location setting
        self.cropLoc = para.cropLoc_MOT
        def cropLoc_update(event):
            self.cropLoc = ast.literal_eval(cropLoc_entry.get())
            cropLoc_res.configure(text='Crop Location = ' + str(self.cropLoc))
        cropLoc_entry = tk.Entry(self.window, textvariable=tk.StringVar(self.window, value=str(self.cropLoc)))
        cropLoc_entry.bind("<Return>", cropLoc_update)
        cropLoc_entry.grid(row=4, column=1)
        cropLoc_res = tk.Label(self.window, text='Crop Location = ' + str(self.cropLoc),  font='Helvetica 12 bold')
        cropLoc_res.grid(row=3, column=1)

        # crop size setting
        def cropsize_update(event):
            self.cropsize = ast.literal_eval(cropsize_entry.get())
            cropsize_res.configure(text='Crop Size = ' + str(self.cropsize))
            self.plot.ax.set_xlim([-self.cropsize/2, self.cropsize/2])
        cropsize_entry = tk.Entry(self.window, textvariable=tk.StringVar(self.window, value=str(self.cropsize)))
        cropsize_entry.bind("<Return>", cropsize_update)
        cropsize_entry.grid(row=1, column=2)
        cropsize_res = tk.Label(self.window, text='Cropsize = ' + str(self.cropsize),  font='Helvetica 12 bold')
        cropsize_res.grid(row=0, column=2)

        # Entries for line locations
        self.linePos = para.linePos
        def linePos_update(event):
            self.linePos = ast.literal_eval(linePos_entry.get())
            linePos_res.configure(text='Line Position = ' + str(self.linePos))
        tk.Label(self.window, text="line positions between 0 to 1").grid(row=5, column=2)
        linePos_entry = tk.Entry(self.window, textvariable=tk.StringVar(self.window, value=str(self.linePos)))
        linePos_entry.bind("<Return>", linePos_update)
        linePos_entry.grid(row=4, column=2)
        linePos_res = tk.Label(self.window, text='Line Position = ' + str(self.linePos), font='Helvetica 12 bold')
        linePos_res.grid(row=3, column=2)

        # Create a canvas that can fit the above video source size
        scale = para.scale_MOT
        self.width, self.height = int(scale * 1262), int(scale * 964)
        self.canvas_img = tk.Canvas(self.window, width=self.width, height=self.height)
        self.canvas_img.grid(row=6, column=0, columnspan=2, rowspan=2)

        # Create a canvas that can fit the slice plot
        self.canvas_slice = FigureCanvasTkAgg(self.plot.fig, master=self.window)
        self.canvas_slice.get_tk_widget().grid(row=6, column=2)

        # Create a canvas that can fit the colourmap plot
        self.canvas_color = tk.Canvas(self.window, width=self.cropcanvassize, height=self.cropcanvassize)
        self.canvas_color.grid(row=7, column=2)

        # for performance testing
        self.time = time.time()
        self.old_time = self.time

        # Starting threads of processes
        thread1 = Thread(target=self.operate_camera)
        thread2 = Thread(target=self.update_feed)
        thread3 = Thread(target=self.update_crop)
        thread1.start()
        thread2.start()
        thread3.start()

    # operate camera
    def operate_camera(self):
        while True:
            self.vid.operate_camera()

            # self.old_time = self.time
            # self.time = time.time()
            # print(self.time-self.old_time)

    # update for video_feed
    def update_feed(self):
        while True:
            frame = self.vid.get_frame()
            feed_frame = self.plot.get_feed(frame, self.cropLoc, self.cropsize, self.width, self.height)
            # Creating display image
            self.photo = PIL.ImageTk.PhotoImage(image=feed_frame)
            self.canvas_img.create_image(0, 0, image=self.photo, anchor=tk.NW)

            # self.old_time = self.time
            # self.time = time.time()
            # print(self.time-self.old_time)

    # update for crop and plot
    def update_crop(self):
        while True:
            # Get a frame from the video source
            frame = self.vid.get_frame()
            # Get update
            cropColor_frame = self.plot.get_plot(frame, self.cropLoc, self.cropsize, self.linePos, self.cropcanvassize)
            # Creating color crop image
            self.cropPhoto = PIL.ImageTk.PhotoImage(image = cropColor_frame)
            self.canvas_color.create_image(0, 0, image=self.cropPhoto, anchor=tk.NW)

            # self.old_time = self.time
            # self.time = time.time()
            # print(self.time-self.old_time)


#####
#Run#
#####

# Create a window and pass it to the Application object
app = App("Profile Viewer")
