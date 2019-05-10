# gupview
The purpose of this package is to create a GUI for the Guppy Pro Camera, extending on the already existing pymba package meant for allied vision cameras which have a commercial GUI named Vimba (which is quite limited).

There are two main scripts within this package:

1. RUN_ME_Flouroscence.py
This code is written with the specific intention of counting the net flouroscence within the specified rectangular area; which dimensions can be adjusted accordingly.

2. RUN_ME_ProfileViewer.py
This code is written with the specific intention of viewing the cross sectional intensity profile from the camera, the cross section locations are depicted by the lines in the colour map plot (see below).

# Packages Required
1. numpy
2. scipy
3. matplotlib
4. PIL
5. cv2; only for applying colour map in /Gupview/Secondary_Scripts/Plots
6. tkinter/Tkinter for python3/2
7. ast

# Additional Notes

1. Both RUN_ME scripts utilises scripts from /Gupview/Secondary_Scripts, and draws parameter values from /Gupview/Parameters.py. Detailed 

2. The flouroscence grab occurs very quickly, and it slows down the live feed update which in turn slows down the flourosence grab. To counter this, the live feed has a timesleep interval, which can be changed in the parameters

3. Sometimes the program has problems starting, saying something like "python has stopped working". But that is okay, just keep restarting
the program until it runs. Tried and tested!

4. Whenever something is keyed into an entry, press <return> in order to activate that value.
  
5. The file save option saves the image you see in the live-feed, without the white rectangular mask.

# Notes on performance

| Exposure [us] | Image Capture [ms] | Livefeed Refresh [ms] | Plot Refresh [ms] | Flourosence Count [ms] |
|:---:|:---:|:---:|:---:|:---:|
| 0.05 | 98 | 23-30 | 52 | 40 |
| 0.1 | 98 | 23-30 | 52 | 40 |
| 10 | 98 | 23-30 | 52 | 40 |
| 1e2 | 98 | 23-30 | 52 | 40 |
| 1e3 | 98 | 23-30 | 52 | 40 |
| 1e4 | 98 | 23-30 | 52 | 40 |

# Screenshots

Screenshot for RUN_ME_Flouroscence.py :

![alt text](https://github.com/BboyTian/Gupview/blob/master/Screenshots/Flouroscence.png)

Screenshot for RUN_ME_ProfileViewer.py :

![alt text](https://github.com/BboyTian/Gupview/blob/master/Screenshots/ProfileViewer.png)


