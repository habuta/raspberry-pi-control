import datetime
import os

def parse_reponse(response):
    res = {i: round(response[i]) for i in response}
    res = {i: res[i] for i in res if res[i] != 0}

    # return the top 3 predictions
    return sorted(res, key=res.get, reverse=True)[:3]

def get_current_video():
    try:
        files = os.listdir("temp/stream")
        if "concat.mp4" in files:
            files.remove("concat.mp4")
        return sorted(files)[-2]
    except IndexError:
        return None
    # return (datetime.datetime.now() - datetime.timedelta(seconds=1)).strftime("%Y-%m-%d_%H:%M:%S")

def get_lastn_videos(n):
    try:
        files = os.listdir("temp/stream")
        if "concat.mp4" in files:
            files.remove("concat.mp4")
        return sorted(os.listdir("temp/stream"))[-n:]
    except IndexError:
        return None
    