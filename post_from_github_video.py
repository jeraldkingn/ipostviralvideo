import os
import requests
import glob
import time

ACCESS_TOKEN = os.getenv("IG_ACCESS_TOKEN")
print("TOKEN:", ACCESS_TOKEN)
IG_USER_ID = os.getenv("IG_USER_ID")
print("USER ID:", IG_USER_ID)

def get_latest_video():
    videos = glob.glob("videos/*.mp4")
    if not videos:
        raise Exception("No videos found in videos folder")

    # pick latest file
    latest = max(videos, key=os.path.getctime)
    return latest

def create_container(video_url):
    print(ACCESS_TOKEN)
    url = f"https://graph.facebook.com/v19.0/{IG_USER_ID}/media"

    payload = {
        "media_type": "VIDEO",
        "video_url": video_url,
        "caption": "Auto posted video 🚀",
        "access_token": ACCESS_TOKEN
    }

    res = requests.post(url, data=payload)
    data = res.json()

    if "id" not in data:
        raise Exception(f"Failed: {data}")

    return data["id"]

def wait(container_id):
    url = f"https://graph.facebook.com/v19.0/{container_id}"

    while True:
        res = requests.get(url, params={
            "fields": "status_code",
            "access_token": ACCESS_TOKEN
        })
        data = res.json()

        if data.get("status_code") == "FINISHED":
            return
        if data.get("status_code") == "ERROR":
            raise Exception(data)

        print("Processing...")
        time.sleep(5)

def publish(container_id):
    url = f"https://graph.facebook.com/v19.0/{IG_USER_ID}/media_publish"

    res = requests.post(url, data={
        "creation_id": container_id,
        "access_token": ACCESS_TOKEN
    })

    return res.json()

if __name__ == "__main__":
    local_file = get_latest_video()

    filename = os.path.basename(local_file)

    video_url = "https://raw.githubusercontent.com/jeraldkingn/ipostviralvideo/main/videos/video1.mp4"
    print("Using:", video_url)

    container = create_container(video_url)
    wait(container)
    result = publish(container)

    print("Posted:", result)