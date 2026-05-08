//event listeners to buttons for connect and pass
document.querySelectorAll(".connect-btn").forEach(function(btn) {
    btn.addEventListener("click", function() {
        handleConnect(this);
    });
});

document.querySelectorAll(".pass-btn").forEach(function(btn) {
    btn.addEventListener("click", function() {
        handlePass(this);
    });
});

function handleConnect(button) {
    const cardContainer = button.closest('.player-card-container');
    
    if (cardContainer) {

        button.disabled = true;
        button.innerHTML = "Request Sent!";
        button.classList.replace('btn-success', 'btn-outline-secondary');

        cardContainer.style.transition = 'all 0.5s ease';
        cardContainer.style.opacity = '0';

        setTimeout(() => {
            cardContainer.remove();
        }, 500);
    }
}

function handlePass(button) {
    const cardContainer = button.closest('.player-card-container');

    if (cardContainer) {

        button.disabled = true;
        button.innerHTML = "Passed!";
        button.classList.replace('btn-danger', 'btn-outline-secondary');

        cardContainer.style.transition = 'all 0.5s ease';
        cardContainer.style.opacity = '0';

        setTimeout(() => {
            cardContainer.remove();
        }, 500);
    }
}