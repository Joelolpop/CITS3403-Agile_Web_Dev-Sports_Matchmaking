const searhInput = document.getElementById('friendSearch');
const friendsList = document.getElementById('friendsList');
const noResults = document.getElementById('noResults');

let setTimeout = null;

searchInput.addEventListener('input', function() {
    clearTimeout(setTimeout);

    searchTimeout = setTimeout(() => {
        const query = searchInput.value.trim();

    })})