from generate_image import generate_image
from openai import OpenAI
from elevenlabs_client import generate_audio
import logging
import time
import json
import base64
import concurrent.futures


logging.basicConfig(filename="./log/assistant.log", level=logging.INFO)


class Assistant:
    def __init__(self, client: OpenAI):
        self.client = client

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
                time.sleep(1)

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
        run = self.client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=self.instance.id,
        )

        self.wait_for_response(thread_id=thread_id, run_id=run.id)

        messages = self.client.beta.threads.messages.list(thread_id=thread_id)
        response_str = self.sanitize_json(
            messages.data[0].content[0].text.value)
        logging.info("(%s) %s: %s", thread_id, messages.data[0].role,
                     response_str)
        response = json.loads(response_str)
        response["thread_id"] = thread_id
        text = response["text"]

        # Generate audio and image concurrently to save some time.
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            audio_future = executor.submit(generate_audio, text)
            new_object = response.get("new_object")
            if new_object is not None and new_object != "":
                new_image_future = executor.submit(
                    self.generate_image, new_object)
                response["new_image"] = new_image_future.result()
            audio = audio_future.result()
            response["audio"] = base64.b64encode(audio).decode("utf-8")
        return response

    def start_thread(self):
        thread = self.client.beta.threads.create()
        return self.send_prompt(thread.id, "Здравей!")
