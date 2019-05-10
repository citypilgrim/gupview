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
from Secondary_Scripts.Flouroscence import Flouro

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

        # initialise flouroscence plot
        self.floursize = para.floursize
        self.flour = Flouro(self.floursize, self.floursize)
        self.cropdimension = para.cropdimension

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
        tk.Label(self.window, text='Save filename', font='Helvetica 12 bold').grid(row=3, column=0)
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
        self.cropLoc = para.cropLoc_flouro
        def cropLoc_update(event):
            self.cropLoc = ast.literal_eval(cropLoc_entry.get())
            cropLoc_res.configure(text='Crop Location = ' + str(self.cropLoc))
        cropLoc_entry = tk.Entry(self.window, textvariable=tk.StringVar(self.window, value=str(self.cropLoc)))
        cropLoc_entry.bind("<Return>", cropLoc_update)
        cropLoc_entry.grid(row=4, column=1)
        cropLoc_res = tk.Label(self.window, text='Crop Location = ' + str(self.cropLoc),  font='Helvetica 12 bold')
        cropLoc_res.grid(row=3, column=1)

        # crop dimension setting
        def cropdimension_update(event):
            self.cropdimension = ast.literal_eval(cropdimension_entry.get())
            cropdimension_res.configure(text='Crop Dimensions = ' + str(self.cropdimension))
        cropdimension_entry = tk.Entry(self.window, textvariable=tk.StringVar(self.window, value=str(self.cropdimension)))
        cropdimension_entry.bind("<Return>", cropdimension_update)
        cropdimension_entry.grid(row=1, column=2)
        cropdimension_res = tk.Label(self.window, text='Crop Dimensions = ' + str(self.cropdimension),  font='Helvetica 12 bold')
        cropdimension_res.grid(row=0, column=2)

        # Entries for flouroscence y limit
        self.ylim = para.ylim
        def ylim_update(event):
            self.ylim = ast.literal_eval(ylim_entry.get())
            ylim_res.configure(text='Y Limit = ' + str(self.ylim))
            self.flour.ax.set_ylim(self.ylim)
        ylim_entry = tk.Entry(self.window, textvariable=tk.StringVar(self.window, value=str(self.ylim)))
        ylim_entry.bind("<Return>", ylim_update)
        ylim_entry.grid(row=1, column=3)
        ylim_res = tk.Label(self.window, text='Y Limit = ' + str(self.ylim), font='Helvetica 12 bold')
        ylim_res.grid(row=0, column=3)

        # Entries for flouroscence y limit
        self.xlim = para.xlim
        def xlim_update(event):
            self.xlim = ast.literal_eval(xlim_entry.get())
            xlim_res.configure(text='Y Limit = ' + str(self.xlim))
        xlim_entry = tk.Entry(self.window, textvariable=tk.StringVar(self.window, value=str(self.xlim)))
        xlim_entry.bind("<Return>", xlim_update)
        xlim_entry.grid(row=4, column=3)
        xlim_res = tk.Label(self.window, text='X Limit = ' + str(self.xlim), font='Helvetica 12 bold')
        xlim_res.grid(row=3, column=3)

        # Value for sum
        tk.Label(self.window, text='Flouroscence Sum = ', font='Helvetica 12 bold').grid(row=3, column=2)
        self.flourSum_res = tk.Label(self.window, text='0E0', font='Helvetica 12 bold')
        self.flourSum_res.grid(row=4, column=2)


        # Create a canvas that can fit the above video source size
        scale = para.scale_flouro
        self.width, self.height = int(scale * 1262), int(scale * 964)
        self.canvas_img = tk.Canvas(self.window, width=self.width, height=self.height)
        self.canvas_img.grid(row=6, column=0, columnspan=2, rowspan=2)

        # Create a canvas that can fit the slice plot
        self.canvas_flour = FigureCanvasTkAgg(self.flour.fig, master=self.window)
        self.canvas_flour.get_tk_widget().grid(row=6, column=2, columnspan=2, rowspan=2)

        # for performance testing
        self.time = time.time()
        self.old_time = self.time

        # Starting threads of processes
        thread1 = Thread(target=self.operate_camera)
        thread2 = Thread(target=self.update_feed)
        thread3 = Thread(target=self.update_flouro)
        thread1.start()
        thread2.start()
        thread3.start()

        self.window.mainloop()

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
            feed_frame = self.flour.get_feed(frame, self.cropLoc, self.cropdimension, self.width, self.height)
            # Creating display image
            self.photo = PIL.ImageTk.PhotoImage(image=feed_frame)
            self.canvas_img.create_image(0, 0, image=self.photo, anchor=tk.NW)

            time.sleep(para.timesleep)

            # self.old_time = self.time
            # self.time = time.time()
            # print(self.time-self.old_time)

    # update for flouroscence plot
    def update_flouro(self):
        while True:
            # Get a frame from the video source
            frame = self.vid.get_frame()
            # Get update
            self.flour.get_plot(frame, self.cropLoc, self.cropdimension, self.xlim, self.flourSum_res)

            # self.old_time = self.time
            # self.time = time.time()
            # print(self.time-self.old_time)


#####
#Run#
#####

# Create a window and pass it to the Application object
app = App("Flouroscence")
