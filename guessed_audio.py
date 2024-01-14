from elevenlabs_client import generate_audio
import base64


guessed_text = "Браво, ти позна!"
guessed_audio_file = "db/guessed.mp3"


def generate_guessed_audio():
    audio = generate_audio(guessed_text)
    with open(guessed_audio_file, "wb") as file:
        file.write(audio)


def base64_guessed_audio():
    with open(guessed_audio_file, "rb") as file:
        audio = file.read()
    return base64.b64encode(audio).decode("utf-8")


if __name__ == "__main__":
    generate_guessed_audio()
