from generate_image import generate_image
from openai import OpenAI
from elevenlabs_client import generate_audio
from pregenerated_audio import guessed_text, start_text
from pregenerated_audio import base64_guessed_audio, base64_start_audio
import logging
import time
import json
import base64
import random


logging.basicConfig(format="%(asctime)s: %(levelname)s: %(message)s",
                    filename="./log/assistant.log",
                    level=logging.INFO)


class Assistant:
    def __init__(self, client: OpenAI, host: str, port: int):
        self.client = client
        self.image_path = f"http://{host}:{port}/images/"

        with open("./db/objects.json", "r") as file:
            self.objects = json.load(file)

    def create_new(self, name: str, instructions: str):
        self.instance = self.client.beta.assistants.create(
            name=name,
            instructions=instructions,
            model="gpt-4-1106-preview"
        )
        with open("./conf/assistant_id.txt", "w") as file:
            file.write(self.instance.id)

    def load_existing(self):
        with open("./conf/assistant_id.txt", "r") as file:
            id = file.read()
        self.instance = self.client.beta.assistants.retrieve(assistant_id=id)

    def wait_for_response(self, thread_id: str, run_id: str):
        while True:
            status = self.client.beta.threads.runs.retrieve(
                thread_id=thread_id,
                run_id=run_id,
            ).status
            if status == "completed":
                break
            else:
                time.sleep(0.3)

    def generate_image(self, object: str):
        return generate_image(self.client, object)

    def sanitize_json(self, json: str):
        ret = json.replace("json", "")
        ret = ret.replace("`", "")
        return ret

    def send_prompt(self, thread_id: str, prompt: str):
        logging.info("(%s) %s: %s", thread_id, "user", prompt)
        self.client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=prompt,
        )
        return self.client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=self.instance.id,
        )

    def send_prompt_and_return_response(self, thread_id: str, prompt: str):
        run = self.send_prompt(thread_id, prompt)

        self.wait_for_response(thread_id=thread_id, run_id=run.id)

        messages = self.client.beta.threads.messages.list(thread_id=thread_id)
        response = messages.data[0].content[0].text.value
        logging.info("(%s) %s: %s", thread_id, messages.data[0].role,
                     response)
        lines = response.splitlines()
        guessed = lines[0]
        json_response = {}
        json_response["thread_id"] = thread_id
        if guessed.startswith("1"):
            new_object = self.select_random_object()
            self.send_prompt(thread_id, "new_object: " + new_object["object"])
            json_response["new_image"] = self.image_url(new_object)
            json_response["text"] = guessed_text
            json_response["audio"] = base64_guessed_audio()
        else:
            hint = lines[1]
            hint = "Опитай пак! " + hint
            json_response["text"] = hint
            audio = generate_audio(hint)
            json_response["audio"] = base64.b64encode(audio).decode("utf-8")
        logging.info("json_response: %s", str(json_response))
        return json_response

    def image_url(self, object):
        return self.image_path + str(object["id"]) + ".jpg"

    def select_random_object(self):
        return random.choice(self.objects)

    def start_thread(self):
        thread = self.client.beta.threads.create()
        new_object = self.select_random_object()
        self.send_prompt(thread.id, "new_object: " + new_object["object"])
        json_response = {}
        json_response["thread_id"] = thread.id
        json_response["new_image"] = self.image_url(new_object)
        json_response["text"] = start_text
        json_response["audio"] = base64_start_audio()
        return json_response
