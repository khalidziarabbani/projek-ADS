// user.js

// Function to toggle between profile and transaction list
function toggleProfile(button) {
    // Get the elements to toggle
    var profileDiv = document.getElementById('profile_div');
    var transactionListDiv = document.getElementById('transaction_list_div');

    // Get the buttons for profile and transaction list
    var profileButton = document.getElementById('profile-btn');
    var transactionListButton = document.getElementById('transaction_list');

    // Check if the button clicked is for profile or transaction list
    if (button.id === 'profile-btn') {
        // Show profile div and hide transaction list div
        profileDiv.classList.add('visible');
        profileDiv.classList.remove('hidden');
        transactionListDiv.classList.add('hidden');
        transactionListDiv.classList.remove('visible');

        // Update button text colors
        profileButton.style.color = 'red';
        transactionListButton.style.color = 'black';
    } else if (button.id === 'transaction_list') {
        // Show transaction list div and hide profile div
        profileDiv.classList.add('hidden');
        profileDiv.classList.remove('visible');
        transactionListDiv.classList.add('visible');
        transactionListDiv.classList.remove('hidden');

        // Update button text colors
        profileButton.style.color = 'black';
        transactionListButton.style.color = 'red';
    }
}

// Add event listeners to the buttons for toggling
document.addEventListener('DOMContentLoaded', function () {
    var profileButton = document.getElementById('profile-btn');
    var transactionListButton = document.getElementById('transaction_list');

    // Set initial state
    profileButton.style.color = 'red';
    transactionListButton.style.color = 'black';
    document.getElementById('profile_div').classList.add('visible');
    document.getElementById('profile_div').classList.remove('hidden');
    document.getElementById('transaction_list_div').classList.add('hidden');
    document.getElementById('transaction_list_div').classList.remove('visible');

    profileButton.addEventListener('click', function () {
        toggleProfile(this);
    });

    transactionListButton.addEventListener('click', function () {
        toggleProfile(this);
    });
});
