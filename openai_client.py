from openai import OpenAI


def get_client():
    with open("./conf/openai_api_key.txt", "r") as file:
        return OpenAI(api_key=file.read(), default_headers={"OpenAI-Beta": "assistants=v2"})
