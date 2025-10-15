// Modal de confirmação de criação da oferta para professores selecionados
(function() {
const form = document.getElementById('peiForm');
const modal = document.getElementById('confirmPeiCreationModal');
const selectedTeachersList = document.getElementById('selectedTeachersList');
const cancelBtn = document.getElementById('cancelModalBtn');
const confirmBtn = document.getElementById('confirmModalBtn');

function onFormSubmit(event) {
    event.preventDefault();

    const checkedTeachers = Array.from(form.querySelectorAll('input[name="teachers"]:checked'));

    if (checkedTeachers.length === 0) {
    alert('Por favor, selecione ao menos um professor.');
    return;
    }

    selectedTeachersList.innerHTML = '';

    checkedTeachers.forEach(input => {
    const parentDiv = input.parentElement;
    let teacherName = '';
    if (parentDiv) {
        const labelEl = parentDiv.querySelector('label');
        let labelText = labelEl ? labelEl.textContent.trim() : '';
        let allText = parentDiv.textContent.trim();
        teacherName = allText.replace(labelText, '').trim();
    }
    if (!teacherName) teacherName = 'Professor desconhecido';

    const li = document.createElement('li');
    li.textContent = teacherName;
    selectedTeachersList.appendChild(li);
    });

    modal.classList.remove('hidden');
    confirmBtn.disabled = true;
    confirmBtn.classList.add('opacity-50', 'cursor-not-allowed');

    let countdown = 7;
    confirmBtn.textContent = `Confirmar (${countdown}s)`;

    const timer = setInterval(() => {
    countdown -= 1;
    confirmBtn.textContent = `Confirmar (${countdown}s)`;

    if (countdown <= 0) {
        clearInterval(timer);
        confirmBtn.disabled = false;
        confirmBtn.textContent = 'Confirmar';
        confirmBtn.classList.remove('opacity-50', 'cursor-not-allowed');
        confirmBtn.focus();
    }
    }, 1000);
}

function confirmAndSubmit() {
    modal.classList.add('hidden');
    form.removeEventListener('submit', onFormSubmit);
    form.submit();
}

function cancelModal() {
    modal.classList.add('hidden');
}

function onKeyDown(event) {
    if (event.key === 'Escape' && !modal.classList.contains('hidden')) {
    cancelModal();
    }
}

form.addEventListener('submit', onFormSubmit);
cancelBtn.addEventListener('click', cancelModal);
confirmBtn.addEventListener('click', confirmAndSubmit);
window.addEventListener('keydown', onKeyDown);
})();
