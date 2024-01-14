const audioPrompt = document.getElementById('audio-prompt');
const chatOutput = document.getElementById('chat-output');
const userInput = document.getElementById('user-input');

const submitGuessButton = document.getElementById('submit-guess');
submitGuessButton.addEventListener('click', submitGuess);

const loader = document.getElementById('spinner');

document.getElementById('start').addEventListener('click', function() {
    audioPrompt.play();
    this.style.display = 'none';
    submitGuessButton.style.display = 'block';
    sendPrompt('startThread', null);
});

let threadId = null;

function updateScroll() {
    chatOutput.scrollTop = chatOutput.scrollHeight;
}

function submitGuess() {
    sendPrompt('sendPrompt', userInput.value);
    chatOutput.innerHTML += `<div>👤: ${userInput.value}</div>`;
    userInput.value = '';
    updateScroll();
}

function sendPrompt(path, prompt) {
    spinner.style.display = 'block';
    let body = {}
    if (prompt !== null) {
        body.thread_id = threadId;
        body.prompt = prompt;
    }
    fetch('http://localhost:5002/' + path, {
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

        if ('audio' in data) {
            audioPrompt.src = "data:audio/mp3;base64," + data.audio;
            audioPrompt.play();
        }
        chatOutput.innerHTML += `<div>🔮: ${data.text}</div>`;
        updateScroll();
        spinner.style.display = 'none';
    })
}

