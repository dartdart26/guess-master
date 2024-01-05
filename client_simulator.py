import requests
import json
import logging
import base64
import subprocess


logging.basicConfig(filename="./log/client_simulator.log", level=logging.INFO)

url = "http://127.0.0.1:5000/"
headers = {"Content-Type": "application/json"}
audio_file_path = "/tmp/client_simulator_audio.mp3"


def client():
    resp = requests.post(url + "startThread").json()
    text = resp["text"]
    new_object = resp.get("new_object")
    image = resp.get("image")
    thread_id = resp["thread_id"]
    logging.info("start thread resp: object=%s, text=%s, image=%s", new_object,
                 text, image)
    print(f"guess-master: {text}")
    play_audio(resp["audio"])
    while True:
        prompt = input("me: ")
        req = {"thread_id": thread_id, "prompt": prompt}
        resp = requests.post(url + "sendPrompt", data=json.dumps(req),
                             headers=headers).json()
        text = resp["text"]
        new_object = resp.get("new_object")
        image = resp.get("image")
        logging.info("prompt resp: object=%s, text=%s, image=%s", new_object,
                     text, image)
        print(f"guess-master: {text}")
        play_audio(resp["audio"])


def play_audio(audio):
    data = base64.b64decode(audio)
    with open(audio_file_path, "wb") as file:
        file.write(data)
    command = ["ffplay", "-nodisp", "-autoexit", audio_file_path]
    process = subprocess.Popen(command, stdout=subprocess.DEVNULL,
                               stderr=subprocess.DEVNULL)
    process.wait()


if __name__ == "__main__":
    client()
