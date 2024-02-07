# guess-master

guess-master is an attempt at using AI for creating a voice and visual conversational tool for children with
certain disabilities.

The main idea is that the guess-master shows DALL-E-generated images to the user and asks them to guess them.
There is a single object in every image. Conversation and choice of object is is handled by a GPT-4 LLM.

Users interact with guess-master via voice and guess-master responds with voice too. Text to speech
is handled by an ElevenLabs model.

An interesting aspect is that we ask GPT-4 to generate JSON documents such that the object
for the image is returned in a separate field and is not mentioned in the response to the user.

## Running
1. Put your OpenAI API key in the `conf/openai_api_key.txt` file.
2. Put your ElevenLabs API key in the `conf/elevenlabs_api_key.txt` file.
3. Create a voice in the ElevenLabs Website and get its ID.
4. Put your ElevenLabs voice ID in the `conf/voice_id.txt` file.
5. Create a virtual environment, e.g. `python3 -m venv path_to_venv`.
6. Activate it, e.g. `source path_to_venv/bin/activate`.
7. Install requirements by `pip install -r requirements.txt`.
8. Optionally, change assistant instructions in `conf/assistant_instructions.txt`.
9. Create an OpenAI assistant by `python ./create_assistant.py`. 
10. Put a list of object (new line separated) in `conf/objets.txt`.
11. Create the folder `db/images`.
12. Generate images by `python ./generate_object_images.py`.
13. Generate sad face/happy face images by `python ./generate_feedback_images.py`.
14. Generate (e.g. in ElevenLabs) an initial voice message and put it as `db/start.mp3`
15. Run the server by `flask --app server run -p 5002`. 
16. Optionally, run the client simulator by `python ./client_simulator.py` or interact with the server in a different way (e.g. Web App).
17. Optinally, open `localhost:5002/index.html` for a web interface.

## Server API

The server exposes two endpoints:
 - **startThread** - starts a fresh new thread and doesn't require any parameters
 - **sendPrompt** - sends a user prompt in an existing thread and requires the following parameters:
    - **thread_id** - the thread ID in which to send the prompt
    - **prompt** - the prompt text

Both endpoints return a JSON with the following fields:
 - **thread_id** - the thread ID the response from guess-master is for
 - **text** - response from guess-master
 - **audio** - a base64-encoded MP3 file of the text from guess-master
 - **new_object** - a decription of a new object if this is the first message in a thread or if the user guessed the previous object and a new one is generated (**new_object** is not present in other cases)
 - **new_image** - an URL to an image of the **new_object** (**new_image** is only present when **new_object** is present)

A thing to note is that the server is stateless itself. State is kept in the OpenAI's thread.

Example request/responses look like:

```json
// startThread request
{}

// startThread response
{
    "thread_id": "abcddd",
    "text": "Yes, this is a cat! What do you think the next object is?",
    "audio": "aabbbbb....",
    "new_object": "big orange baloon",
    "new_image": "http://...."
}
```

```json
// sendPrompt request with a correct guess 
{
    "thread_id": "abcddd",
    "prompt": "I think this is a cat!"
}

// sendPrompt response for a correct guess
{
    "thread_id": "abcddd",
    "text": "Yes, this is a cat! What do you think the next object is?",
    "audio": "aabbbbb....",
    "new_object": "big orange baloon",
    "new_image": "http://...."
}
```

```json
// sendPrompt request with an incorrect guess 
{
    "thread_id": "abcddd",
    "prompt": "I think this is a cat!"
}

// sendPrompt response for an incorrect guess and a hint
{
    "thread_id": "abcddd",
    "text": "Nope, this is not a cat. It is a much bigger animal. What do you think it is?",
    "audio": "aabbbbb....",
}
```

## Frontend
The frontend runs on voice recognition by default. This works only in Chrome/Edge/Safari. However the chat history as well as a text field to write and a submit button can be used by clicking of the "Слушам те!" label in the main screen of the game.