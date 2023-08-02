console.log('main.js is loaded successfully!');
// copyright year
const date = new Date();
document.querySelector('.year').innerHTML = date.getFullYear();


// Function to update the current date and time
function updateCurrentDateTime() {
    const currentDate = new Date().toLocaleDateString(); // Get the current date in the user's locale
    const currentTime = new Date().toLocaleTimeString(); // Get the current time in the user's locale
    const currentDateTime = `${currentDate} ${currentTime}`; // Combine date and time
    document.querySelector('.current-date-time').innerHTML = currentDateTime; // Update the content of the element with the current date and time
}

// Call the function once when the page is loaded to display the initial date and time
updateCurrentDateTime();


// message alert
setTimeout(function () {
    $('#message').fadeOut('slow');
}, 3000);

// toggle password for login and register
function showPassword1() {
    var x = document.getElementById("myPassword1");
    if (x.type === "password") {
        x.type = "text";
    } else {
        x.type = "password";
    }
}

function showPassword2() {
    var x = document.getElementById("myPassword2");
    if (x.type === "password") {
        x.type = "text";
    } else {
        x.type = "password";
    }
}

