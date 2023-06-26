import cv2
import numpy as np
import datetime
from concurrent.futures import ThreadPoolExecutor
import time

IP = "0.0.0.0"
PORT = 5000
url = f"http://{IP}:{PORT}/video_feed"
EXPORT_PATH = "temp/stream"
FRAME_RATE = 30  # adjust this according to your video stream
FRAME_DURATION = 1 / FRAME_RATE  
NUM_FRAMES = 2 * FRAME_RATE  # total frames for a 2 second video

def save_clip(frames, name, frame_rate):
    # Define the codec using VideoWriter_fourcc and create a VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(f"{EXPORT_PATH}/{name}.mp4", fourcc, frame_rate, (frames[0].shape[1], frames[0].shape[0]))

    for frame in frames:
        out.write(frame)

    out.release()

def get_frames(url):
    stream = cv2.VideoCapture(url)
    frames = []
    frame_count = 0

    if stream.isOpened():
        while True:
            (grabbed, frame) = stream.read()
            if not grabbed:
                print("Frame not grabbed")
                break

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frames.append(frame)
            frame_count += 1

            if frame_count >= NUM_FRAMES:
                break
    else:
        print("Unable to open video stream")

    stream.release()
    return frames

with ThreadPoolExecutor(max_workers=2) as executor:
    while True:
        frames = get_frames(url)
        name = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
        future = executor.submit(save_clip, frames, name, FRAME_RATE)
        while future.running():
            time.sleep(1)  # introduce a delayz to lower resource usage
