import math
import os
import shutil
import sys

from PIL import Image

os.mkdir('/tmp/frames')

frames = 224
save_dir = sys.argv[1]

if not save_dir:
    print("You must specify a directory to save the video to!")
    sys.exit()

for frame in range(frames):
    redpos = (frame + 112, 112) if frame <= 111 else None
    bluepos = (frame - ((frame - 112) * 2), 112) if frame >= 112 else None

    background = Image.new(mode='RGB', size=(224, 224), color=(255, 255, 255))
    red_square = Image.new(mode='RGB', size=(10, 10), color=(255, 0, 0))
    blue_square = Image.new(mode='RGB', size=(10, 10), color=(0, 0, 255))

    if redpos:
        background.paste(red_square, redpos)
    else:
        background.paste(blue_square, bluepos)
    background.save(f'/tmp/frames/frame{frame}.jpg')

os.system(f"cd /tmp/frames && ffmpeg -r 60 -i frame%d.jpg {save_dir}/video.mp4")
print(f"Saved video to {save_dir}")

shutil.rmtree("/tmp/frames")