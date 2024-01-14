from openai import OpenAI
import logging


def generate_image(client: OpenAI, object: str):
    logging.info("generating image: %s", object)
    resp = client.images.generate(
        model="dall-e-3",
        prompt=object,
        size="1024x1024",
        quality="standard",
        n=1
    )
    url = resp.data[0].url
    logging.info("generated image: %s", url)
    return url
