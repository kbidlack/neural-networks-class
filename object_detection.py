import os
import shutil
import sys

import cv2
import fastbook
from fastai.vision.core import PILImage
from PIL import Image, ImageDraw, ImageFont


learn = fastbook.load_learner("model.pkl") # load model


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


def predict(image):
    """Predict if an image has a red or blue square"""

    pred_class, pred_idx, probabilities = learn.predict(image)
    return pred_class


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

    font = ImageFont.truetype('Arial.ttf')

    for i in range(len(frames)):
        image = f'/tmp/frames/frame{i}.jpg'
        predicted = predict(image) # returns either 'red', 'blue', or 'white'

        pimage = Image.open(f'/tmp/frames/frame{i}.jpg')
        pimagedraw = ImageDraw.Draw(pimage)
        # add text to the image
        pimagedraw.text(xy=(112, 8), 
                        text=str(predicted), 
                        fill=(0, 0, 0), 
                        font=font,
                        anchor='ms')

        pimage.save(f'/tmp/newframes/frame{i}.jpg')
    
    os.system(f"cd /tmp/newframes && ffmpeg -r 60 -i frame%d.jpg {save_dir}/detected.mp4 2> /dev/null") # save the final video
    print(f"Saved video to {save_dir}")

    shutil.rmtree('/tmp/frames')
    shutil.rmtree('/tmp/newframes')