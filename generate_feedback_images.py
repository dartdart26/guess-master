from generate_image import generate_image
import openai_client
import requests

client = openai_client.get_client()


def generate_sad_image():
    url = generate_image(client, "sad face suitable for children")
    image = requests.get(url)
    with open("./db/images/sad.jpg", "wb") as image_file:
        image_file.write(image.content)


def generate_guessed_image():
    url = generate_image(client, "very happy face suitable for children - "
                         "make it very colourful")
    image = requests.get(url)
    with open("./db/images/guessed.jpg", "wb") as image_file:
        image_file.write(image.content)


if __name__ == "__main__":
    generate_sad_image()
    generate_guessed_image()
