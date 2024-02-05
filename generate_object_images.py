from generate_image import generate_image
from tqdm import tqdm
import openai_client
import json
import logging
import requests

client = openai_client.get_client()
logging.basicConfig(format="%(asctime)s: %(levelname)s: %(message)s",
                    filename="./log/generate_object_images.log",
                    level=logging.INFO)


def generate_object_images():
    objects_db = []
    with open("./conf/objects.txt", "r") as file:
        objects = [obj.strip() for obj in file]
    id = 0
    for obj in tqdm(objects, desc="Generating images"):
        logging.info("generating image for object (%s), id (%d)", obj, id)
        url = generate_image(client, obj)
        logging.info("generated image for object(%s), id(%d): %s",
                     obj, id, url)
        objects_db.append({"id": id, "object": obj, "original_url": url})
        image = requests.get(url)
        with open(f"./db/images/{id}.jpg", "wb") as image_file:
            image_file.write(image.content)
        id += 1
    with open("./db/objects.json", "w") as file:
        json.dump(objects_db, file, indent=4)


if __name__ == "__main__":
    generate_object_images()
