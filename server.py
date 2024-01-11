from assistant import Assistant
from flask import Flask, request, jsonify, send_from_directory
import openai_client


app = Flask(__name__)
assistant = Assistant(openai_client.get_client())
assistant.load_existing()


@app.route("/startThread", methods=["POST"])
def start_thread():
    resp = assistant.start_thread()
    return jsonify(resp)


@app.route("/sendPrompt", methods=["POST"])
def send_prompt():
    req = request.get_json()
    thread_id = req["thread_id"]
    prompt = req["prompt"]
    resp = assistant.send_prompt(thread_id, prompt)
    return jsonify(resp)


@app.route("/<path:path>", methods=["GET"])
def serve(path):
    return send_from_directory("frontend", path)


if __name__ == "__main__":
    app.run()
