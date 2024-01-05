import requests
import json
import logging


logging.basicConfig(filename="./log/client_simulator.log", level=logging.INFO)

url = "http://127.0.0.1:5000/"
headers = {"Content-type": "application/json"}


def client():
    start_thread_resp = requests.post(url + "startThread").json()
    logging.info("start thread resp: %s", start_thread_resp)
    thread_id = start_thread_resp["thread_id"]
    text = start_thread_resp["text"]
    print(f"guess-master: {text}")
    while True:
        prompt = input("me: ")
        req = {"thread_id": thread_id, "prompt": prompt}
        resp = requests.post(url + "sendPrompt", data=json.dumps(req),
                             headers=headers).json()
        logging.info("prompt resp: %s", resp)
        text = resp["text"]
        print(f"guess-master: {text}")


if __name__ == "__main__":
    client()
