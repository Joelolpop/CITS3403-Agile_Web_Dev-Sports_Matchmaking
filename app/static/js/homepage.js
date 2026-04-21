function handleAuth(type) {
    if (type === 'su') {
        console.log('signing up...');
    } else {
        console.log('logging in...');
    }
}

function switchTab(tab) {
    const suForm = document.getElementById('formsu');
    const liForm = document.getElementById('formli');
    const tabSu = document.getElementById('tabsu');
    const tabLi = document.getElementById('tabli');

    if (tab === 'su') {
        suForm.classList.remove('hidden');
        liForm.classList.add('hidden');
        tabSu.classList.add('active');
        tabLi.classList.remove('active');
    } else {
        liForm.classList.remove('hidden');
        suForm.classList.add('hidden');
        tabLi.classList.add('active');
        tabSu.classList.remove('active');
    }
}