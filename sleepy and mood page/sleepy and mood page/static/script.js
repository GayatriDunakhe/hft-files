// // Update this code within script.js
// const moodSelect = document.getElementById('moodSelect');
// const sleepySelect = document.getElementById('sleepySelect');

// // Function to send data to the Flask server and get the duration
// function calculateDuration() {
//     const mood = moodSelect.value;
//     const sleepiness = sleepySelect.value;

//     // Send the selected data to the server
//     fetch('/calculate_duration', {
//         method: 'POST',
//         body: JSON.stringify({ mood, sleepiness }),
//         headers: {
//             'Content-Type': 'application/json',
//         },
//     })
//     .then(response => response.json())
//     .then(data => {
//         alert(`Mood duration: ${data.moodDuration} seconds\nSleepiness duration: ${data.sleepinessDuration} seconds`);
//     })
//     .catch(error => console.error(error));
// }

// // Add an event listener to a button or trigger to call calculateDuration
// // You can create a button in your HTML and add a click event listener to trigger this function.

// // Example button in your HTML:
// // <button id="calculateButton">Calculate Duration</button>

// Example event listener:
// document.getElementById('calculateButton').addEventListener('click', calculateDuration);
