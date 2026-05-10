const searchInput = document.getElementById('friendSearch');
const friendsList = document.getElementById('friendsList');
const noResults = document.getElementById('noResults');

let searchTimeout = null;

searchInput.addEventListener('input', function() {
    clearTimeout(searchTimeout);

    searchTimeout = setTimeout(() => {
        const query = searchInput.value.trim();

        fetch(`/friends/search?q=${encodeURIComponent(query)}`)
            .then(response => response.json())
            .then(data => {
                friendsList.innerHTML = '';

                if (data.friends.length === 0) {
                    noResults.style.display = 'block';
                    return;
                }

                noResults.style.display = 'none';

                data.friends.forEach(friend => {
                    const sports = friend.sports.map(sport =>
                        `<span class="badge bg-dark text-success border border-success" style="font-size: 0.8em;">${sport}</span>`
                    ).join(' ');

                    friendsList.innerHTML += `
                        <div class="card h-100 border-success shadow-sm" style="background: var(--background-nav);">
                            <div class="card-body d-flex flex-column">
                                <div class="d-flex align-items-center mb-3">
                                    <div>
                                        <h5 class="mb-0 text-white">${friend.username || friend.first_name}</h5>
                                        <small class="text-secondary">${friend.postcode || "No postcode"}</small>
                                    </div>
                                </div>

                                <div class="mb-3">
                                    <label class="small text-secondary d-block mb-1">Sports:</label>
                                    <div class="d-flex flex-wrap gap-1">
                                        ${sports || '<span class="text-secondary small">No sports selected.</span>'}
                                    </div>
                                </div>

                                <a href="{{ url_for('main.friend_data', friend_id=friend.user_id) }}" class="btn btn-outline-success btn-sm mt-auto">View Profile</a>
                            </div>
                        </div>`
                });
            })
            .catch(error => 
                console.error('Search error:', error));
    }, 300);
});