from assistant import Assistant
from openai_client import get_client
import sys
import logging


def test_start_thread():
    client = get_client()
    assistant = Assistant(client)

    if sys.argv[1] == "create":
        with open("./conf/assistant_instructions.txt", "r") as file:
            instructions = file.read()
        assistant.create_new("guess-master", instructions)
    elif sys.argv[1] == "load":
        with open("./conf/assistant_id.txt", "r") as file:
            assistant_id = file.read()
        assistant.load_existing(assistant_id)
    else:
        exit(-1)

    resp = assistant.start_thread()
    print(resp)
    thread_id = resp["thread_id"]
    resp = assistant.send_prompt(thread_id=thread_id, content="телефон")
    print(resp)
    resp = assistant.send_prompt(thread_id=thread_id, content="телефон")
    print(resp)


def test_correct_guess():
    client = get_client()
    assistant = Assistant(client)
    with open("./conf/assistant_id.txt", "r") as file:
        assistant_id = file.read()
        assistant.load_existing(assistant_id)

    thread_id = "thread_QJ1foO27vtmyueQLegbfrd75"
    resp = assistant.send_prompt(thread_id=thread_id, content="топка")
    print(resp)


if __name__ == "__main__":
    logging.basicConfig(filename="./log/assistant.log", level=logging.INFO)
    test_start_thread()
