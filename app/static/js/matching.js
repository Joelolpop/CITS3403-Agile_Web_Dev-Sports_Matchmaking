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
