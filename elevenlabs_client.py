import requests


with open("./conf/elevenlabs_api_key.txt", "r") as file:
    api_key = file.read()
with open("./conf/voice_id.txt", "r") as file:
    voice_id = file.read()
chunk_size = 1024
url = "https://api.elevenlabs.io/v1/text-to-speech/" + voice_id
headers = {
    "xi-api-key": api_key,
    "Content-Type": "application/json",
    "Accept": "audio/mpeg"
}


def generate_audio(text: str):
    data = {
        "text": text,
        "model": "eleven_monolingual_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5
        }
    }
    response = requests.post(url, json=data, headers=headers)
    return response.content


if __name__ == "__main__":
    generate_audio("Здравей, аз съм Оракулът!")
