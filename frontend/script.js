const baseUrl = 'http://localhost:5002/';

const startContainer    = document.getElementById('start-container');
const gameLoader        = document.getElementById('game-loader');
const gameContainer     = document.getElementById('game-container');
const startButton       = document.getElementById('start');
const audioPrompt       = document.getElementById('audio-prompt');
const chatContainer     = document.getElementById('chat-container');
const chatOutput        = document.getElementById('chat-output');
const userInput         = document.getElementById('user-input');
const image             = document.getElementById('object-image');
const submitGuessButton = document.getElementById('submit-guess');
const cannonsContainer  = document.getElementById('cannons');
const cannons           = document.getElementsByClassName('cannon');
const cannonSound       = document.getElementById('cannon-sound');
const applauseSound     = document.getElementById('applause-sound');
const chatToggle        = document.getElementById('toggle-chat');


chatToggle.addEventListener('click', () => {
    chatContainer.classList.toggle('hidden')
});

submitGuessButton.addEventListener('click', submitGuess);

startButton.addEventListener('click', () => {
    audioPrompt.play();
    sendPrompt('startThread', null);
});

let threadId = null;
let firstRun = true;

if ('webkitSpeechRecognition' in window) {
    var speechRecognition = new webkitSpeechRecognition();
    speechRecognition.lang = 'bg-BG';
    speechRecognition.interimResults = true;
    speechRecognition.maxAlternatives = 1;
    speechRecognition.continuous = true;

    speechRecognition.onresult = (event) => {
        var speechResult = event.results[0][0].transcript;
        document.getElementById('user-input').value = speechResult;
        
        if (event.results[0].isFinal) {
            submitGuess();
        }
    };

    speechRecognition.onerror = (event) => {
        console.log('Грешка в разпознаването на глас.', event.error);
        speechRecognition.start();
    };
} else {
    console.log('За съжаление, този браузър не поддържа разпознване на глас. Моля опитайте с Google Chrome или Microsoft Edge.');
}

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
    speechRecognition.stop();

    startContainer.style.display = 'none';
    gameContainer.style.display = 'none';
    gameLoader.style.display = 'flex';

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
            if (firstRun == true) {
                image.src = data.new_image;
                firstRun = false;
            } else {
                image.src = baseUrl + 'images/guessed.jpg';
                fireAllCannons();

                setTimeout(() => {
                    image.src = data.new_image;
                }, 7000);
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

        gameLoader.style.display = 'none';    
        gameContainer.style.display = 'block';
        speechRecognition.start();
    })
}

function fireCannon(cannon, timesLeft) {
    if (timesLeft <= 0) {
      return;
    }
  
    let interval = Math.random() * 500 + 500;
  
    setTimeout(() => {
      party.confetti(cannon, {
        shapes: ["star"],
        count: 50,
        size: 2.5,
        speed: 900,
        spread: 40,
        color: new party.Color.fromHex("#ffd700"),
      });
      
      cannonSound.currentTime = 0;
      cannonSound.play();
      
      fireCannon(cannon, timesLeft - 1);
    }, interval);
  }


function fireAllCannons() {
    let firesCount = 5;

    applauseSound.currentTime = 0;
    applauseSound.volume = 0.4; 
    applauseSound.play();

    cannonsContainer.style.display = 'block'; 
    [...cannons].forEach(cannon => fireCannon(cannon, firesCount));
    setTimeout(() => { cannonsContainer.style.display = 'none' }, firesCount * 1000);
}

