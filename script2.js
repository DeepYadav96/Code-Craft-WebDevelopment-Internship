let startTime = 0;
let elapsedTime = 0;
let timerInterval;
let running = false;

const display = document.getElementById('display');
const startBtn = document.getElementById('start');
const pauseBtn = document.getElementById('pause');
const resetBtn = document.getElementById('reset');
const lapBtn = document.getElementById('lap');
const lapsList = document.getElementById('laps');

function formatTime(ms) {
    const centiseconds = Math.floor((ms % 1000) / 10);
    const seconds = Math.floor((ms / 1000) % 60);
    const minutes = Math.floor((ms / (1000 * 60)) % 60);
    const hours = Math.floor(ms / (1000 * 60 * 60));
    return (
        (hours < 10 ? '0' : '') + hours + ':' +
        (minutes < 10 ? '0' : '') + minutes + ':' +
        (seconds < 10 ? '0' : '') + seconds + '.' +
        (centiseconds < 10 ? '0' : '') + centiseconds
    );
}

function updateDisplay() {
    display.textContent = formatTime(elapsedTime);
}

function startTimer() {
    if (!running) {
        running = true;
        startTime = Date.now() - elapsedTime;
        timerInterval = setInterval(() => {
            elapsedTime = Date.now() - startTime;
            updateDisplay();
        }, 10);
    }
}

function pauseTimer() {
    if (running) {
        running = false;
        clearInterval(timerInterval);
    }
}

function resetTimer() {
    running = false;
    clearInterval(timerInterval);
    elapsedTime = 0;
    updateDisplay();
    lapsList.innerHTML = '';
}

function addLap() {
    if (running) {
        const li = document.createElement('li');
        li.textContent = formatTime(elapsedTime);
        lapsList.appendChild(li);
    }
}

function getRandomColor() {
    
    return '#' + Math.floor(Math.random() * 16777215).toString(16).padStart(6, '0');
}

function changeButtonColor(e) {
    e.target.style.backgroundColor = getRandomColor();
    e.target.style.color = getRandomColor();
    e.target.style.borderColor = getRandomColor();
}

startBtn.addEventListener('click', function (e) {
    startTimer();
    changeButtonColor(e);
});
pauseBtn.addEventListener('click', function (e) {
    pauseTimer();
    changeButtonColor(e);
});
resetBtn.addEventListener('click', function (e) {
    resetTimer();
    changeButtonColor(e);
});
lapBtn.addEventListener('click', function (e) {
    addLap();
    changeButtonColor(e);
});

updateDisplay();
