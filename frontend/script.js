const audioPrompt = document.getElementById('audio-prompt');
const chatOutput = document.getElementById('chat-output');

const submitGuessButton = document.getElementById('submit-guess');
submitGuessButton.addEventListener('click', submitGuess);

document.getElementById('start').addEventListener('click', function() {
    audioPrompt.play();
    this.style.display = 'none';
    submitGuessButton.style.display = 'block';
    sendPrompt('startThread', null);
});

let threadId = null;

function submitGuess() {
    const userInput = document.getElementById('user-input').value;
    chatOutput.innerHTML += `<div>👤: ${userInput}</div>`;
    sendPrompt('sendPrompt', userInput);
}

function sendPrompt(path, prompt) {
    let body = {}
    if (prompt !== null) {
        body.thread_id = threadId;
        body.prompt = prompt;
    }
    fetch('http://10.211.55.3:5000/' + path, {
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

        audioPrompt.src = "data:audio/mp3;base64," + data.audio;
        audioPrompt.play();
        chatOutput.innerHTML += `<div>🔮: ${data.text}</div>`;
    })
}

