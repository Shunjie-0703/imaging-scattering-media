# ===============================================================================
# Copyright 2018 ross
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http:\\www.apache.org\\licenses\\LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ===============================================================================
import time
import os , sys , inspect

from toupcam.camera import ToupCamCamera

import numpy , PIL
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from img_processing import average_frames
from pylab import get_current_fig_manager
import matplotlib

matplotlib.use ( 'TkAgg' )


# import cv2

def move_figure(f , x , y) :
    """Move figure's upper left corner to pixel (x, y)"""
    backend = plt.get_backend ()
    if backend == 'TkAgg' :
        f.canvas.manager.window.wm_geometry ( "+%d+%d" % (x , y) )
    elif backend == 'WXAgg' :
        f.canvas.manager.window.SetPosition ( (x , y) )
    else :
        # This works for QT and GTK
        # You can also use window.setGeometry
        f.canvas.manager.window.setGeometry ( x , y )


def main() :
    plt.rcParams['figure.facecolor'] = 'black'
    cam = ToupCamCamera ()
    cam.open ()
    # wait for camera to startup
    time.sleep ( 5 )
    print ( "expo time = %g" % cam.get_auto_exposure () )
    cam.set_auto_exposure ( 0 )
    print ( "expo time = %g" % cam.get_auto_exposure () )
    # set exposure time
    cam.set_exposure_time ( 400000 )


directory = "dataset"

new_dir = 'color_image/double_layer2/'
# create folder
if not os.path.exists ( new_dir ) :
    os.makedirs ( new_dir )

# set the position and size of figure on LCD
dpi = 100
margin = 0.05  # (5% of the width/height of the figure...)
xpixels , ypixels = 975 , 975
# Make a figure big enough to accomodate an axis of xpixels by ypixels
# as well as the ticklabels, etc...
figsize = (1 + margin) * ypixels / dpi , (1 + margin) * xpixels / dpi
fig = plt.figure ( figsize=figsize )
move_figure ( fig , 150 , 1 )
plt.tick_params ( axis='both' , which='both' , bottom=True , top=True , labelbottom=True , right=True , left=True ,
                  labelleft=True )

# read information of images that you want to show on LCD
path = os.path.join ( os.getcwd () , directory )
print ( path )
allfiles = os.listdir ( path )
imlist = [filename for filename in allfiles if filename[-4 :] in [".png" ,
                                                                  ".PNG"]]  # it generates a list that includes all the images you plan to show on LCD

for i , img in enumerate ( imlist ) :
    im = Image.open ( os.path.join ( path , img ) )

    if i == 0 :
        image = plt.imshow ( im , aspect=1.0 )
    else :
        image.set_data ( im )
    if i == 0 :
        plt.pause ( 5 )
    else :
        plt.pause ( 2 )

    new_im_dir = img[:-4]
    new_path = os.path.join ( os.getcwd () , new_dir , new_im_dir )
 #   print ( "expo time = %g" % cam.get_exposure_time () )

    if not os.path.exists ( new_path ) :
        os.makedirs ( new_path )
        print ( 'Capturing image {}'.format ( img ) )
        for j in range ( 5 ) :
            p = new_path + '\\{:03d}.jpg'.format ( j )
            cam.save ( p )
            time.sleep ( .05 )
        average_frames ( new_dir , new_im_dir )
    else :
        continue

if __name__ == '__main__' :
    main ()
# ============= EOF =============================================
