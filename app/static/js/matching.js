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
    const csrfTokenMeta = document.querySelector('meta[name="csrf-token"]');
    const csrfToken = csrfTokenMeta ? csrfTokenMeta.getAttribute('content') : null;
    
    if (!receiverId) {
        alert("Could not send request. Please refresh and try again.");
        return;
    }

    button.disabled = true;

    fetch('/friends/request', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken || ''
        },
        body: JSON.stringify({ receiver_id: receiverId })
    })
    .then(async (response) => {
        const contentType = response.headers.get('content-type') || '';
        const data = contentType.includes('application/json')
            ? await response.json()
            : { ok: false, message: 'Request failed. Please refresh and try again.' };

        return { ok: response.ok, data };
    })
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