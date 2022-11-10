# Neural Networks Class
Simple object detection using ai, for a class.

To use, run main.py with the video as the first argument and the save directory as the second argument:
```py
python main.py "/Users/kavi/Desktop/video.mp4" "/Users/kavi/Desktop" # will save the file to my Desktop, as 'predicted.mp4'
```
To generate a sample video, run the generate_video script with a destination:
```py
python generate_video.py "/Users/kavi/Desktop" # will save the video to my Desktop, as 'video.mp4'
```
If it fails, you may have to delete the /tmp/frames folder on your computer and try again
