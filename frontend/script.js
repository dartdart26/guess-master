const audioPrompt = document.getElementById('audio-prompt');
const chatOutput = document.getElementById('chat-output');
const userInput = document.getElementById('user-input');
const image = document.getElementById('object-image');

const submitGuessButton = document.getElementById('submit-guess');
submitGuessButton.addEventListener('click', submitGuess);

const loader = document.getElementById('spinner');
const baseUrl = 'http://localhost:5002/';

document.getElementById('start').addEventListener('click', function() {
    audioPrompt.play();
    this.style.display = 'none';
    submitGuessButton.style.display = 'block';
    sendPrompt('startThread', null, false);
});

let threadId = null;

function updateScroll() {
    chatOutput.scrollTop = chatOutput.scrollHeight;
}

function submitGuess() {
    sendPrompt('sendPrompt', userInput.value, true);
    chatOutput.innerHTML += `<div>👤: ${userInput.value}</div>`;
    userInput.value = '';
    updateScroll();
}

function createConfetti() {
    const confettiCount = 200;
    const confettiContainer = document.createElement("div");
    for (let i = 0; i < confettiCount; i++) {
        const confetti = document.createElement("div");
        confetti.className = "confetti-piece";
        confetti.style.left = `${Math.random() * 100}%`;
        confetti.style.top = `${Math.random() * 100}%`;
        confetti.style.backgroundColor = getRandomColor();
        confettiContainer.append(confetti);
    }
    document.body.appendChild(confettiContainer);

    setTimeout(() => {
        document.body.removeChild(confettiContainer);
    }, 2000);
}

function getRandomColor() {
    const colors = ["#ff0", "#f0f", "#0ff", "#0f0", "#00f", "#foo"];
    return colors[Math.floor(Math.random() * colors.length)];
}

function sendPrompt(path, prompt, confetti) {
    spinner.style.display = 'block';
    let body = {}
    if (prompt !== null) {
        body.thread_id = threadId;
        body.prompt = prompt;
    }
    fetch(baseUrl + path, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(body)
    })
    .then(response => response.json())
    .then(data => {
        if ('new_image' in data) {
            if (confetti) {
                createConfetti();
                image.src = baseUrl + 'images/guessed.jpg';
                setTimeout(() => {
                    image.src = data.new_image;
                }, 2000);
            } else {
                image.src = data.new_image;
            }
        } else {
            const currentImage = image.src;
            image.src = baseUrl + 'images/sad.jpg';
            setTimeout(() => {
                image.src = currentImage;
            }, 2000);
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

