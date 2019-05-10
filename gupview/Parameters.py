# Common Parameters
save_dir = 'Z:/Data/2019/'  # default saving directory
camera_index = 0 # default camera to use

#RUN_ME_MOTviewer.py params
cropLoc_MOT = (int(1024 / 2), int(768 / 2)) # location of crop box
cropsize = 50  # box crop side length, each pixel is 3.75um
linePos = (0.5, 0.5) # default starting line positions
scale_MOT = 0.5 # the size of the live feed display; value is between 0 to 1
plotsize = 380 # the default size of the plot display
cropcanvassize = 380 # the default size of the crop colormap display

# RUN_ME_Flouroscence.py params
floursize = 300 # size of flouroscence plot
scale_flouro = 0.3 # the size of the live feed display; value is between 0 to 1
cropLoc_flouro = (int(1024 / 2), int(768 / 2)) # location of crop box
cropdimension = (50, 100) # default dimensions of the crop box
ylim = (0, 5e3) # y limit of flourosence plot
xlim = 40 # x limit of previous flourosence viewed
timesleep = 0.1 # this limits the framerate of the live-feed