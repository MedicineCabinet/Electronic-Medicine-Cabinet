// static/idleLogout.js

const IDLE_TIMEOUT = 60; // Idle time in seconds (1 minute)
let idleTime = 0;

const timerIncrement = () => {
    idleTime += 1;
    if (idleTime >= IDLE_TIMEOUT) {
        window.location.href = "/logout?idle=true";
    }
};

const resetTimer = () => {
    idleTime = 0;
};

const initializeIdleTimer = () => {
    document.body.addEventListener('mousemove', resetTimer);
    document.body.addEventListener('keypress', resetTimer);
    setInterval(timerIncrement, 1000);
};

document.addEventListener('DOMContentLoaded', initializeIdleTimer);
