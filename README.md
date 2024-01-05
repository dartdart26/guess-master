# guess-master

guess-master is an attempt at using AI for creating a voice and visual conversational tool for children with
certain disabilities.

The main idea is that the guess-master shows DALL-E-generated images to the user and asks them to guess it.
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
5. Activate it, e.g. `source path_to_venv/bin/activate`.
6. Install requirements by `pip install -r requirements.txt`.
7. Create an OpenAI assistant by `python ./create_assistant.py`.
8. Run the server by `flask --app server run`. 
9. Optionally, run the client simulator by `python ./client_simulator.py` or interact with the server in a different way (e.g. Web App).

## Server API

The server exposes two endpoints:
 - startThread - starts a fresh new thread and doesn't require any parameters
 - sendPrompt - sends a user prompt in an existing thread and requires the following parameters:
    - thread_id - the thread ID in which to send the prompt
    - prompt - the prompt text

Both endpoints return a JSON with the following fields:
 - thread_id - the thread ID the response from guess-master is for
 - text - response from guess-master
 - audio - a base64-encoded MP3 file of the text from guess-master
 - new_object - a decription of a new object if this is the first message in a thread or if the user guessed the previous object and a new one is generated (new_object is not present in other cases)
 - image - an URL to an image of the new_object (image only present when new_object is present)

A thing to note is that the server is stateless itself. State is kept in the OpenAI's thread.

An example request/response looks like:
```json
// sendPrompt request
{
    "thread_id": "abcddd",
    "prompt": "I think this is a cat!"
}

// sendPrompt response
{
    "thread_id": "abcddd",
    "text": "Yes, this is a cat! What do you think the next object is?",
    "audio": "aabbbbb....",
    "new_object": "big orange baloon",
    "image: "http://...."
}
```
