import requests
import logging


with open("./conf/elevenlabs_api_key.txt", "r") as file:
    api_key = file.read()
with open("./conf/voice_id.txt", "r") as file:
    voice_id = file.read()
url = "https://api.elevenlabs.io/v1/text-to-speech/" + voice_id + "/stream"
headers = {
    "xi-api-key": api_key,
    "Content-Type": "application/json",
    "Accept": "audio/mpeg"
}


params = dict()
params["output_format"] = "mp3_22050_32"
params["optimize_streaming_latency"] = 4


def generate_audio(text: str):
    data = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5
        }
    }
    logging.info("sending request to ElevenLabs")
    response = requests.post(url, json=data, headers=headers, params=params)
    logging.info("received response from ElevenLabs")
    return response.content


if __name__ == "__main__":
    generate_audio("Здравей, аз съм Оракулът!")
