import math
import os
import shutil
import sys
from random import randint, random
from tkinter import filedialog

import cv2
from PIL import Image

import scanner


def create_frames():
    video_path = sys.argv[1]
    print(f"Using video {video_path}")
    capture = cv2.VideoCapture(video_path)
    total_video_frames = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))

    print(f"Generating frames from video: {video_path}")
    frame_number = 0
    
    while True:
        # process frames
        success, frame = capture.read()

        if frame_number % 60 == 0:
            print(f"Splitting frames... {frame_number}/{total_video_frames}")

        if success:
            cv2.imwrite(f"/tmp/frames/frame{frame_number}.jpg", frame)
        else:
            break # finish loop at the end of the video

        frame_number += 1
    
    print(f"Splitting frames... {frame_number}/{total_video_frames}")


def add_line(img, x1, y1, x2, y2):
    point = Image.new(mode='RGB', size=(1, 1), color=(0, 255, 0))

    for iy in range(y2 - y1 + 1):
        y = y1 + iy
        for ix in range(x2 - x1 + 1):
            x = x1 + ix
            img.paste(point.resize((2,2)), [x, y])
    return img


if __name__ == "__main__":
    # temporary folder for split frames
    try:
        os.mkdir('/tmp/frames')
        create_frames()
    except FileExistsError: # use pre-processed frames
        delete_tmp_frames = input("/tmp/frames exists. Overwrite it? (y/n) ")
        if delete_tmp_frames == "y":
            shutil.rmtree('/tmp/frames')
            os.mkdir('/tmp/frames')
            create_frames()
        elif delete_tmp_frames == "n":
            print("Using frames specified in /tmp/frames.")
    
    try:
        shutil.rmtree('/tmp/newframes')
        os.mkdir('/tmp/newframes')
    except FileNotFoundError:
        os.mkdir('/tmp/newframes')

    frames = os.listdir('/tmp/frames')
    save_dir = sys.argv[2]
    
    point = Image.new(mode='RGB', size=(4, 4), color=(0, 255, 0)) # object pos indicator

    for i in range(len(frames)):
        pimage = Image.open(f'/tmp/frames/frame{i}.jpg')
        found_points = scanner.scanImage(pimage)

        # draw box around object
        pimage = add_line(pimage, found_points[0][0], found_points[0][1], found_points[1][0], found_points[0][1])
        pimage = add_line(pimage, found_points[0][0], found_points[1][1], found_points[1][0], found_points[1][1])
        pimage = add_line(pimage, found_points[0][0], found_points[0][1], found_points[0][0], found_points[1][1])
        pimage = add_line(pimage, found_points[1][0], found_points[0][1], found_points[1][0], found_points[1][1])
        pimage.save(f'/tmp/newframes/frame{i}.jpg')
        
    os.system(f"cd /tmp/newframes && ffmpeg -r 60 -i frame%d.jpg {save_dir}/tracked.mp4 2> /dev/null")
    print(f"Saved video to {save_dir}")

    shutil.rmtree('/tmp/frames')
    shutil.rmtree('/tmp/newframes')