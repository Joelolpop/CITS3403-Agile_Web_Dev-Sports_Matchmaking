const chips = document.querySelectorAll('.sport-chip');
const sportCount = document.getElementById('sport-count');
const sportHidden = document.getElementById('sport-hidden');
const selected = [];

function renderSelectedState() {
	chips.forEach(function (chip) {
		const sport = chip.getAttribute('data-sport');
		if (selected.includes(sport)) {
			chip.classList.remove('btn-outline-success');
			chip.classList.add('btn-success');
		} else {
			chip.classList.remove('btn-success');
			chip.classList.add('btn-outline-success');
		}
	});

	sportCount.textContent = selected.length + ' / 3 selected';
	sportHidden.value = selected.join(',');
}

if (sportHidden.value.trim()) {
	sportHidden.value.split(',').forEach(function (sport) {
		const trimmedSport = sport.trim();
		if (trimmedSport && selected.length < 3 && !selected.includes(trimmedSport)) {
			selected.push(trimmedSport);
		}
	});
}

renderSelectedState();

chips.forEach(function (chip) {
	chip.onclick = function () {
		const sport = chip.getAttribute('data-sport');
		const idx = selected.indexOf(sport);

		if (idx !== -1) {
			selected.splice(idx, 1);
			chip.classList.remove('btn-success');
			chip.classList.add('btn-outline-success');
		} else if (selected.length < 3) {
			selected.push(sport);
			chip.classList.remove('btn-outline-success');
			chip.classList.add('btn-success');
		} else {
			alert('You can select up to 3 sports only.');
		}

		renderSelectedState();
	};
});
