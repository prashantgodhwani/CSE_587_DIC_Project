// Initializing an empty array 'selectedCards'
let selectedCards = [];

// Querying all elements with class 'card-cuisine'
const cards = document.querySelectorAll('.card-cuisine');

// Adding event listener to each card
cards.forEach(card => {
    card.addEventListener('click', () => {
        card.classList.toggle('selected');

        // Getting the id of the clicked card
        const cardId = card.dataset.id;
        console.log(cardId);

        // Checking if the id of the clicked card already exists in 'selectedCards' array
        if (selectedCards.includes(cardId)) {
            // Removing the id from the array
            selectedCards = selectedCards.filter(id => id !== cardId);
        } else {
            // Adding the id to the array
            selectedCards.push(cardId);
        }
        console.log(selectedCards);
    });

});

// Adding click event listener to 'recommend' button
const saveAndRedirect = document.querySelector('#recommend');
saveAndRedirect.addEventListener('click', () => {
    if (selectedCards.length > 0) {
        // Saving user id and selected cuisine cards to local storage
        localStorage.setItem('userId', document.getElementById('user-id').value);
        localStorage.setItem('cuisines', selectedCards);
        // Redirecting to 'home.html'
        window.location = 'home.html';
        return
    } else return
});
