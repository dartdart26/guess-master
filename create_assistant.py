from assistant import Assistant
from openai_client import get_client


def create_assistant():
    with open("./conf/assistant_instructions.txt", "r") as file:
        instructions = file.read()
    client = get_client()
    assistant = Assistant(client)
    assistant.create_new("guess-master", instructions)
    print(f"created assistant with ID {assistant.instance.id}")


if __name__ == "__main__":
    create_assistant()
