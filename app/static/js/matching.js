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
    const receiverId = button.dataset.userId;
    
    if (!receiverId) {
        alert("Could not send request. Please refresh and try again.");
        return;
    }

    button.disabled = true;

    fetch('/friends/request', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ receiver_id: receiverId })
    })
    .then((response) => response.json().then((data) => ({ ok: response.ok, data })))
    .then(({ ok, data }) => {
        if (!ok || !data.ok) {
            throw new Error(data.message || 'Failed to send request.');
        }

        button.innerHTML = "Request Sent!";
        button.classList.replace('btn-outline-success', 'btn-outline-secondary');

        if (cardContainer) {
        cardContainer.style.transition = 'all 0.5s ease';
        cardContainer.style.opacity = '0';

        setTimeout(() => {
            cardContainer.remove();
        }, 500);
        }
    })
    .catch((error) => {
        button.disabled = false;
        alert(error.message);
    });
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