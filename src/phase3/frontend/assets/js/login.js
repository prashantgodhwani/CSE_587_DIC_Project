// This code block adds an event listener to the "sign-in" button, and sets the userId in localStorage before redirecting to the home page
document.getElementById('sign-in').addEventListener('click', () => {
    const userId = document.getElementById('user-id').value;
    localStorage.clear();
    localStorage.setItem('userId', userId);
    window.location.href = 'home.html';
});

// This code block adds an event listener to the "Create Account" link and redirects to the cuisine-selection page when clicked
const createAccountLink = document.querySelector('#newUser');

createAccountLink.addEventListener('click', () => {
    window.location.href = 'cuisine-selection.html';
});