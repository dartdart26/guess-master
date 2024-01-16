from elevenlabs_client import generate_audio
import base64


guessed_text = "Браво, ти позна!"
guessed_audio_file = "db/guessed.mp3"
start_text = "Нека започвме! Какво виждаш?"
start_audio_file = "db/start.mp3"


def generate_guessed_audio():
    audio = generate_audio(guessed_text)
    with open(guessed_audio_file, "wb") as file:
        file.write(audio)


def generate_start_audio():
    audio = generate_audio(start_text)
    with open(start_audio_file, "wb") as file:
        file.write(audio)


def base64_audio(file):
    with open(file, "rb") as f:
        audio = f.read()
    return base64.b64encode(audio).decode("utf-8")


def base64_guessed_audio():
    return base64_audio(guessed_audio_file)


def base64_start_audio():
    return base64_audio(start_audio_file)


if __name__ == "__main__":
    generate_guessed_audio()
    generate_start_audio()
