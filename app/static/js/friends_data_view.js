document.getElementById('removeFriendBtn').addEventListener('click', function() {
    const friendId = this.getAttribute('data-friend-id');
    const redirectUrl = this.getAttribute('data-friend-url');
    const csrfTokenMeta = document.querySelector('meta[name="csrf-token"]');
    const csrfToken = csrfTokenMeta ? csrfTokenMeta.getAttribute('content') : null;
    
     this.disabled = true;

    fetch(`/friends/${friendId}/remove`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken || ''
        }
    })
    .then(res => res.json())
    .then(data => {
        if (data.ok) {
            // Safely hide the modal
            const modalEL = document.getElementById('removeFriendModal');
            const modal = bootstrap.Modal.getInstance(modalEL);
            if (modal) {
                modal.hide();
            }
            
            window.location.href = redirectUrl;
        } else {
            alert(data.message);
            this.disabled = false;
        }
    });
});