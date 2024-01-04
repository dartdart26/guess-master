from dalle import generate_image
from openai import OpenAI
import logging
import time
import json


class Assistant:
    def __init__(self, client: OpenAI):
        self.client = client

    def create_new(self, name: str, instructions: str):
        self.assistant = self.client.beta.assistants.create(
            name=name,
            instructions=instructions,
            model="gpt-4-1106-preview"
        )
        with open("./conf/assistant_id.txt", "w") as file:
            file.write(self.assistant.id)

    def load_existing(self, id: str):
        self.assistant = self.client.beta.assistants.retrieve(assistant_id=id)

    def wait_for_response(self):
        # TODO
        time.sleep(10)

    def generate_image(self, object: str):
        return generate_image(self.client, object)

    def sanitize_json(self, json: str):
        ret = json.replace("json", "")
        ret = ret.replace("`", "")
        return ret

    def send_prompt(self, thread_id: str, content: str):
        logging.info("(%s) %s: %s", thread_id, "user", content)
        self.client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=content,
        )
        run = self.client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=self.assistant.id,
        )
        self.client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run.id,
        )
        self.wait_for_response()
        messages = self.client.beta.threads.messages.list(thread_id=thread_id)
        response_str = self.sanitize_json(
            messages.data[0].content[0].text.value)
        logging.info("(%s) %s: %s", thread_id, messages.data[0].role,
                     response_str)
        response = json.loads(response_str)
        object = response["object"]
        if response["guessed"]:
            new_image_url = self.generate_image(object)
            return {
              "thread_id": thread_id,
              "object": object,
              "image": new_image_url,
            }
        else:
            return {
              "thread_id": thread_id,
              "object": object,
            }

    def start_thread(self):
        thread = self.client.beta.threads.create()
        return self.send_prompt(thread.id, "Здравей!")
