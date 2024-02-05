const baseUrl = 'http://localhost:5002/';

const startContainer    = document.getElementById('start-container');
const gameLoader        = document.getElementById('game-loader');
const gameContainer     = document.getElementById('game-container');
const startButton       = document.getElementById('start');
const audioPrompt       = document.getElementById('audio-prompt');
const chatOutput        = document.getElementById('chat-output');
const userInput         = document.getElementById('user-input');
const image             = document.getElementById('object-image');
const submitGuessButton = document.getElementById('submit-guess');
const cannonsContainer  = document.getElementById('cannons');
const cannons           = document.getElementsByClassName('cannon');
const cannonSound       = document.getElementById('cannon-sound');
const applauseSound     = document.getElementById('applause-sound');

submitGuessButton.addEventListener('click', submitGuess);

startButton.addEventListener('click', function() {
    audioPrompt.play();
    sendPrompt('startThread', null);
});

let threadId = null;
let firstRun = true;

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
