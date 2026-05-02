document.getElementById('removeFriendBtn').addEventListener('click', function() {
    const friendId = this.getAttribute('data-friend-id');
    const redirectUrl = this.getAttribute('data-friend-url');
    
    if (confirm('Are you sure you want to remove this friend?')) {

        this.disabled = true;

        setTimeout(() => {
            window.location.href = redirectUrl;
        }, 800);
    }
});