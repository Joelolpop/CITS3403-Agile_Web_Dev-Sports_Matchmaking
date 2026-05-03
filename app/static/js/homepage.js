
// Handle authentication actions (also switches to create event view after auth)
function handleAuth(type) {
    if (type === 'su') {
        console.log('signing up...');
    } else {
        console.log('logging in...');
    }
    document.getElementById('auth-box').classList.add('d-none');
    document.getElementById('create-box').classList.remove('d-none');
}

//tab switcher-changes tab when pressing on signup or login
function switchTab(tab) {
    const suForm = document.getElementById('formsu');
    const liForm = document.getElementById('formli');
    const tabSu = document.getElementById('tabsu');
    const tabLi = document.getElementById('tabli');

    if (tab === 'su') {
        suForm.classList.remove('d-none');
        liForm.classList.add('d-none');
        tabSu.classList.add('text-success', 'border', 'border-success', 'fw-semibold');
        tabSu.classList.remove('text-secondary');
        tabSu.style.background = 'var(--green-glow)';
        tabLi.classList.remove('text-success', 'border', 'border-success', 'fw-semibold');
        tabLi.classList.add('text-secondary');
        tabLi.style.background = 'transparent';
    } else {
        liForm.classList.remove('d-none');
        suForm.classList.add('d-none');
        tabLi.classList.add('text-success', 'border', 'border-success', 'fw-semibold');
        tabLi.classList.remove('text-secondary');
        tabLi.style.background = 'var(--green-glow)';
        tabSu.classList.remove('text-success', 'border', 'border-success', 'fw-semibold');
        tabSu.classList.add('text-secondary');
        tabSu.style.background = 'transparent';
    }
}


//Swaps emojis to make it look like an animation.
const emos = document.querySelectorAll('.emo');
let cur = 0;
setInterval(() => {
    emos[cur].classList.remove('active');
    cur = (cur + 1) % emos.length;
    emos[cur].classList.add('active');
}, 2000);