import requests
from constants import STABLEDIFFUSION_BASE_URL, TXT2IMG
import base64
import uuid

BASE_PROMPT = {
    "negative_prompt": "BadDream, UnrealisticDream, nsfw, nudity",
    "steps": 40,
    "do_not_save_samples": True,
    "do_not_save_grid": True,
}


def txt2image_request(prompt: str, uuid_str: str, ind: int):
    url = STABLEDIFFUSION_BASE_URL + TXT2IMG
    data = BASE_PROMPT
    data["prompt"] = prompt
    response = requests.post(url, json=data)

    response = response.json()

    imageList = response['images']

    for index, image in enumerate(imageList):
        with open(f"outputs/{uuid_str}-{ind}.png", "wb") as f:
            f.write(base64.b64decode(image))

    response["uuid"] = uuid_str
    return response
