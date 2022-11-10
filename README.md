# Neural Networks Class
Simple object detection and tracking using fastai. This was a project for a class.

[Object Detection](./object-detection.py) attempts to detect an object.
[Object Tracking](./object-tracking.py) attempts to track the position of the object.
The model is pretrained on red and blue squares.

## Usage
To generate a sample video, run the generate-video script with a destination:
```py
python generate_video.py "/Users/kavi/Desktop"
```

To use, run either [object-detection](./object-detection.py) or [object-tracking](./object-tracking.py) with the video as the first argument and the save directory as the second argument:
```py
python object-detection.py "/Users/kavi/Desktop/sample_video.mp4" "/Users/kavi/Desktop"
```
The above command will save a detected video file to my Desktop, as 'detected.mp4'

Similarly,
```py
python object-detection.py "/Users/kavi/Desktop/sample_video.mp4" "/Users/kavi/Desktop" # will save the file to my Desktop, as 'detected.mp4'
```
will save a tracked video file to my Desktop, as 'tracked.mp4'

## Credits
Thanks to [Speckeyeam](https://www.github.com/speckeyeam) for training the model and [ItchyTrack](https://www.github.com/ItchyTrack) for writing the object tracker ([scanner.py](./scanner.py)).