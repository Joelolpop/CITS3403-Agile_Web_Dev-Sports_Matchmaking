document.getElementById('removeFriendBtn').addEventListener('click', function() {
    const friendId = this.getAttribute('data-friend-id');
    const redirectUrl = this.getAttribute('data-friend-url');
    const csrfTokenMeta = document.querySelector('meta[name="csrf-token"]');
    const csrfToken = csrfTokenMeta ? csrfTokenMeta.getAttribute('content') : null;
    
    if (confirm('Are you sure you want to remove this friend?')) {

        this.disabled = true;

        fetch(`/friends/${friendId}/remove`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken || ''
            }
        })
        .then(() => {
            window.location.href = redirectUrl;
        });
    }
});