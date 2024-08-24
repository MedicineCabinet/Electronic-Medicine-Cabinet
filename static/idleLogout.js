// static/idleLogout.js

let idleTime = 0;

// Increment the idle time counter every second.
const timerIncrement = () => {
    idleTime += 1;
    if (idleTime > 59) { // 1 minute
        window.location.href = "/logout"; // Redirect to logout
    }
};

// Reset the idle timer on mouse movement or key press
const resetTimer = () => {
    idleTime = 0;
};

// Set up event listeners to reset the timer on activity
window.onload = function () {
    document.body.addEventListener('mousemove', resetTimer);
    document.body.addEventListener('keypress', resetTimer);
};

// Set the interval to check idle time every second (1000 ms)
setInterval(timerIncrement, 1000);
