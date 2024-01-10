document.getElementById('submit-guess').addEventListener('click', submitGuess);

let threadId = null;

function submitGuess() {
    const userInput = document.getElementById('user-input').value;
    const chatOutput = document.getElementById('chat-output');
    chatOutput.innerHTML += `<div>Ти предположи: ${userInput}</div>`;
    sendPrompt('sendPrompt', userInput)
}

function sendPrompt(path, prompt) {
    let body = {}
    if (prompt !== null) {
        body.thread_id = threadId
        body.prompt = prompt
    }
    fetch('http://127.0.0.1:5000/' + path, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(body)
    })
    .then(response => response.json())
    .then(data => {
        if ('new_image' in data) {
            document.getElementById('object-image').src = data.new_image;
        }
        threadId = data.thread_id;
        const audioPrompt = document.getElementById('audio-prompt');
        audioPrompt.src = "data:audio/mp3;base64," + data.audio;
        audioPrompt.play();
    })
}

sendPrompt('startThread', null)
