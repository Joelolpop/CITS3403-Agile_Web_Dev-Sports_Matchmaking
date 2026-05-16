const searchInput = document.getElementById('friendSearch');
const friendsList = document.getElementById('friendsList');
const noResults = document.getElementById('noResults');
const searchResults = document.getElementById('searchResults');

let searchTimeout = null;

searchInput.addEventListener('input', function() {
    clearTimeout(searchTimeout);

    searchTimeout = setTimeout(() => {
        const query = searchInput.value.trim();

        if (!query) {
            friendsList.style.display = '';
            searchResults.style.display = 'none';
            noResults.style.display = 'none';
            return;
        }

        fetch(`/friends/search?q=${encodeURIComponent(query)}`)
            .then(response => response.json())
            .then(data => {
                friendsList.style.display = 'none';
                searchResults.innerHTML = '';

                if (data.friends.length === 0) {
                    searchResults.style.display = 'none';
                    noResults.style.display = 'block';
                    return;
                }

                noResults.style.display = 'none';
                searchResults.style.display = '';

                data.friends.forEach(friend => {
                    const sports = friend.sports.map(sport =>
                        `<span class="badge bg-dark text-success border border-success" style="font-size: 0.8em;">${sport}</span>`
                    ).join(' ');

                    searchResults.innerHTML += `
                    <div class="col-12 col-md-6">
                        <div class="card h-100 border-success shadow-sm" style="background: var(--background-nav);">
                            <div class="card-body d-flex flex-column">
                                <div class="d-flex align-items-center mb-3">
                                    <div>
                                        <h5 class="mb-0 text-success fw-semibold">${ friend.username } <span class="text-white">- ${friend.first_name } ${friend.last_name }</span></h5>
                                        <small class="text-secondary">${friend.postcode || "No postcode"}</small>
                                    </div>
                                </div>

                                <div class="mb-3">
                                    <label class="small text-secondary d-block mb-1">Sports:</label>
                                    <div class="d-flex flex-wrap gap-1">
                                        ${sports || '<span class="text-secondary small">No sports selected.</span>'}
                                    </div>
                                </div>

                                <a href="/friends/${friend.user_id}" class="btn btn-outline-success btn-sm mt-auto">View Profile</a>
                            </div>
                        </div>
                    </div>`;
                });
            })
            .catch(error => 
                console.error('Search error:', error));
    }, 300);
});