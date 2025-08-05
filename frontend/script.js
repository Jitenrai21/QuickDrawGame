// Get references to the HTML elements
const startScreen = document.getElementById("start-screen");
const gameScreen = document.getElementById("game-screen");
const postGameScreen = document.getElementById("post-game-screen");
const startButton = document.getElementById("start-button");
const restartButton = document.getElementById("restart-button");
const timeLeftDisplay = document.getElementById("time-left");
const currentObjectDisplay = document.getElementById("current-object");
const objectPlaceholder = document.getElementById("object-placeholder");
const clearButton = document.getElementById("clear-button");
const canvas = document.getElementById("drawing-canvas");
const ctx = canvas.getContext("2d");

let drawing = false;
let lastX = 0;
let lastY = 0;
let timeLeft = 30;
let timer;

// Array to hold the sequence of drawing coordinates
let drawingData = [];

// Set canvas size
canvas.width = 600;
canvas.height = 400;

// Placeholder for object to draw
const objectToDraw = "Cat"; // Placeholder object

// Show start screen
startButton.addEventListener("click", startGame);

// Timer function
function startTimer() {
    timer = setInterval(() => {
        timeLeft--;
        timeLeftDisplay.textContent = timeLeft;
        if (timeLeft <= 0) {
            clearInterval(timer);
            endGame();
        }
    }, 1000);
}

// Start the game by hiding start screen and showing the game screen
function startGame() {
    startScreen.style.display = "none";
    gameScreen.style.display = "block";
    currentObjectDisplay.textContent = objectToDraw; // Display object to draw
    startTimer();
}

// Draw on the canvas
canvas.addEventListener("mousedown", startDrawing);
canvas.addEventListener("mousemove", draw);
canvas.addEventListener("mouseup", stopDrawing);
canvas.addEventListener("mouseout", stopDrawing);
canvas.addEventListener("touchstart", startDrawing);
canvas.addEventListener("touchmove", draw);
canvas.addEventListener("touchend", stopDrawing);

function startDrawing(e) {
    drawing = true;
    [lastX, lastY] = getCoordinates(e);
}

function draw(e) {
    if (!drawing) return;
    const [x, y] = getCoordinates(e);
    
    // Store the drawing coordinates
    drawingData.push({ x, y });
    
    ctx.beginPath();
    ctx.moveTo(lastX, lastY);
    ctx.lineTo(x, y);
    ctx.strokeStyle = "#000";
    ctx.lineWidth = 5;
    ctx.stroke();
    [lastX, lastY] = [x, y];
}

function stopDrawing() {
    drawing = false;
}

// Get coordinates for touch or mouse events
function getCoordinates(e) {
    if (e.touches) {
        return [e.touches[0].clientX - canvas.offsetLeft, e.touches[0].clientY - canvas.offsetTop];
    } else {
        return [e.offsetX, e.offsetY];
    }
}

// Clear canvas on button click
clearButton.addEventListener("click", clearCanvas);

function clearCanvas() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    drawingData = [];  // Clear the drawing data when clearing the canvas
}

// End game after timer
function endGame() {
    gameScreen.style.display = "none";
    postGameScreen.style.display = "block";
    sendDrawingData();  // Send the drawing data to the backend
    document.getElementById("model-guess").textContent = "Time's up!";
}

// Function to send the drawing data to the backend for recognition
function sendDrawingData() {
    const data = {
        drawing: drawingData,  // Send the captured drawing data (coordinates)
        object: objectToDraw,  // Include the object to draw as part of the data (optional)
    };

    // Send the drawing data to the backend using fetch
    fetch("/api/recognize-drawing", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(data),  // Send the drawing data as JSON
    })
    .then(response => response.json())
    .then(data => {
        // Handle the response (e.g., show model's prediction or time's up message)
        console.log(data);
        document.getElementById("model-guess").textContent = `Model Prediction: ${data.prediction}`;
    })
    .catch(error => {
        console.error("Error sending drawing data:", error);
    });
}

// Restart game by resetting everything
restartButton.addEventListener("click", restartGame);

function restartGame() {
    postGameScreen.style.display = "none";
    startScreen.style.display = "block";
    timeLeft = 30;
    timeLeftDisplay.textContent = timeLeft;
    drawingData = [];  // Clear the drawing data for a new game
    clearCanvas();
}
