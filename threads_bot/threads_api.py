import requests
import time
import logging
from config import THREADS_ACCESS_TOKEN, THREADS_USER_ID

log = logging.getLogger(__name__)
BASE = "https://graph.threads.net/v1.0"

def _params(**kwargs):
    return {"access_token": THREADS_ACCESS_TOKEN, **kwargs}

def create_post(text):
    # Step 1: Create container
    resp = requests.post(
        f"{BASE}/{THREADS_USER_ID}/threads",
        params=_params(media_type="TEXT", text=text)
    )
    resp.raise_for_status()
    creation_id = resp.json()["id"]
    log.info(f"發文容器建立：{creation_id}")

    time.sleep(5)

    # Step 2: Publish
    resp = requests.post(
        f"{BASE}/{THREADS_USER_ID}/threads_publish",
        params=_params(creation_id=creation_id)
    )
    resp.raise_for_status()
    post_id = resp.json()["id"]
    log.info(f"發文成功，Post ID：{post_id}")
    return post_id

def reply_to_comment(comment_id, text):
    # Step 1: Create reply container
    resp = requests.post(
        f"{BASE}/{THREADS_USER_ID}/threads",
        params=_params(media_type="TEXT", text=text, reply_to_id=comment_id)
    )
    resp.raise_for_status()
    creation_id = resp.json()["id"]

    time.sleep(3)

    # Step 2: Publish reply
    resp = requests.post(
        f"{BASE}/{THREADS_USER_ID}/threads_publish",
        params=_params(creation_id=creation_id)
    )
    resp.raise_for_status()
    return resp.json()["id"]

def get_my_posts(limit=10):
    resp = requests.get(
        f"{BASE}/{THREADS_USER_ID}/threads",
        params=_params(fields="id,text,timestamp", limit=limit)
    )
    resp.raise_for_status()
    return resp.json().get("data", [])

def get_replies(post_id):
    resp = requests.get(
        f"{BASE}/{post_id}/replies",
        params=_params(fields="id,text,username,timestamp")
    )
    resp.raise_for_status()
    return resp.json().get("data", [])
