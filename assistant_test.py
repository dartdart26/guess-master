from assistant import Assistant
import openai_client
import sys


def test_start_thread():
    client = openai_client.get_client()
    assistant = Assistant(client)

    if sys.argv[1] == "create":
        with open("./conf/assistant_instructions.txt", "r") as file:
            instructions = file.read()
        assistant.create_new("guess-master", instructions)
    elif sys.argv[1] == "load":
        assistant.load_existing()
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
    client = openai_client.get_client()
    assistant = Assistant(client)
    assistant.load_existing()

    thread_id = "thread_QJ1foO27vtmyueQLegbfrd75"
    resp = assistant.send_prompt(thread_id=thread_id, content="топка")
    print(resp)


if __name__ == "__main__":
    test_start_thread()
