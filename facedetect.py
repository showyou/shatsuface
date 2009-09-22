#!/usr/bin/env python
"""
This program is demonstration for face and object detection using haar-like features.
The program finds faces in a camera image or video stream and displays a red box around them.

Original C implementation by:  ?
Python implementation by: Roman Stanchak
"""
import sys
import os
from opencv.cv import *
from opencv.highgui import *

# Global Variables
#SAMPLE = True
SAMPLE = False
cascade = None
storage = cvCreateMemStorage(0)
cascade_name = "./haarcascades/haarcascade_frontalface_alt.xml"
input_name = "./facedata/face/lena.jpg"

# Parameters for haar detection
# From the API:
# The default parameters (scale_factor=1.1, min_neighbors=3, flags=0) are tuned 
# for accurate yet slow object detection. For a faster operation on real video 
# images the settings are: 
# scale_factor=1.2, min_neighbors=2, flags=CV_HAAR_DO_CANNY_PRUNING, 
# min_size=<minimum possible face size
min_size = cvSize(20,20)
image_scale = 1.3
haar_scale = 1.2
min_neighbors = 2
haar_flags = 0

starFlag = False
def detect_and_draw( img,cascade ):
    gray = cvCreateImage( cvSize(img.width,img.height), 8, 1 );
    small_img = cvCreateImage( cvSize( cvRound (img.width/image_scale),
						               cvRound (img.height/image_scale)), 8, 1 );
    cvCvtColor( img, gray, CV_BGR2GRAY );
    cvResize( gray, small_img, CV_INTER_LINEAR );

    cvEqualizeHist( small_img, small_img );
    
    cvClearMemStorage( storage );
    faceFlag = False
    if( cascade ):
        t = cvGetTickCount();
        faces = cvHaarDetectObjects( small_img, cascade, storage,
                                     haar_scale, min_neighbors, haar_flags, min_size );
        t = cvGetTickCount() - t;
        print "detection time = %gms" % (t/(cvGetTickFrequency()*1000.));
        if faces:
            for r in faces:
                print "detect face!"
                faceFlag = True
                pt1 = cvPoint( int(r.x*image_scale), int(r.y*image_scale))
                pt2 = cvPoint( int((r.x+r.width)*image_scale), int((r.y+r.height)*image_scale) )
                cvRectangle( img, pt1, pt2, CV_RGB(255,0,0), 3, 8, 0 );

    cvShowImage( "result", img );
    return faceFlag

import re
import Image
from cStringIO import StringIO
import urllib
def getImageUrl2File(filename):
    str1 = filename.split("?")[0]
    re1 = re.match("http://[\w\W]*/([\w\W]+)",str1)
    if re1:
         saveName = re1.group(1)
    print saveName
    buffer = urllib.urlopen(filename).read()
    image = Image.open(StringIO(buffer))
    image.save("./img/"+saveName)
    return saveName

def miniFaceDetect(fileNames):

    cascade = cvLoadHaarClassifierCascade( cascade_name, cvSize(1,1) );
    if not cascade:
        print "ERROR: Could not load classifier cascade"
        sys.exit(-1)
    #cvNamedWindow( "result", 1 );

    for root,dirs,files in os.walk("./img"):
        for f in files:
            os.remove("./img/"+f)
    result = []
    if SAMPLE:
        fileNames = ['./facedata/face/20090828185252.jpg','./facedata/face/20090915160926.jpg','./facedata/face/20090918165256.jpg','./facedata/face/20090918165734.jpg']
    for fileName in fileNames:
        if SAMPLE:
            input_name = fileName
        else:
            try:  
                input_name = getImageUrl2File(fileName[1])
            except IOError:
                print "ERROR: Can not open Photo:",fileName[1]
                continue
        capture = cvCreateFileCapture( input_name ); 
        
        if SAMPLE:
            image = cvLoadImage(input_name,1);
        else:
		    image = cvLoadImage( "./img/"+input_name, 1 );
        
        if( image ):
            if detect_and_draw( image, cascade ):
                result.append(fileName);
            #cvWaitKey(0);

    #cvDestroyWindow("result");
    return result


def main(input_name):
    # the OpenCV API says this function is obsolete, but we can't
    # cast the output of cvLoad to a HaarClassifierCascade, so use this anyways
    # the size parameter is ignored
    cascade = cvLoadHaarClassifierCascade( cascade_name, cvSize(1,1) );
    
    if not cascade:
        print "ERROR: Could not load classifier cascade"
        sys.exit(-1)

    if input_name.isdigit():
        capture = cvCreateCameraCapture( int(input_name) )
    else:
        capture = cvCreateFileCapture( input_name ); 

    cvNamedWindow( "result", 1 );

    if( capture ):
        frame_copy = None
        while True: 
            frame = cvQueryFrame( capture );
            if( not frame ):
                break;
            if( not frame_copy ):
                frame_copy = cvCreateImage( cvSize(frame.width,frame.height),
                                            IPL_DEPTH_8U, frame.nChannels );
            if( frame.origin == IPL_ORIGIN_TL ):
                cvCopy( frame, frame_copy );
            else:
                cvFlip( frame, frame_copy, 0 );
            
            detect_and_draw( frame_copy,cascade );

            if( cvWaitKey( 10 ) >= 0 ):
                break;

    else:
        image = cvLoadImage( input_name, 1 );

        if( image ):
        
            detect_and_draw( image,cascade );
            cvWaitKey(0);
        
    cvDestroyWindow("result");

if __name__ == '__main__':

    if len(sys.argv) > 1:

        if sys.argv[1].startswith("--cascade="):
            cascade_name = sys.argv[1][ len("--cascade="): ]
            if len(sys.argv) > 2:
                input_name = sys.argv[2]

        elif sys.argv[1] == "--help" or sys.argv[1] == "-h":
            print "Usage: facedetect --cascade=\"<cascade_path>\" [filename|camera_index]\n" ;
            sys.exit(-1)

        else:
            input_name = sys.argv[1]

    main(input_name)
