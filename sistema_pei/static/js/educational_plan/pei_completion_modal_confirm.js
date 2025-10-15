(function() {
  const modal = document.getElementById('confirmPeiCompletionModal');
  const cancelBtn = document.getElementById('cancelCompletionBtn');
  const confirmBtn = document.getElementById('confirmCompletionBtn');
  const markCompletedBtn = document.getElementById('markCompletedBtn');

  let countdownTimer;

  function startCountdown() {
    confirmBtn.disabled = true;
    confirmBtn.classList.add('opacity-50', 'cursor-not-allowed');
    let countdown = 7;
    confirmBtn.textContent = `Confirmar (${countdown}s)`;

    countdownTimer = setInterval(() => {
      countdown -= 1;
      confirmBtn.textContent = `Confirmar (${countdown}s)`;
      if (countdown <= 0) {
        clearInterval(countdownTimer);
        confirmBtn.disabled = false;
        confirmBtn.textContent = 'Confirmar';
        confirmBtn.classList.remove('opacity-50', 'cursor-not-allowed');
      }
    }, 1000);
  }

  if (markCompletedBtn) {
    markCompletedBtn.addEventListener('click', () => {
      modal.classList.remove('hidden');
      startCountdown();
    });
  }

  if (cancelBtn) {
    cancelBtn.addEventListener('click', () => {
      modal.classList.add('hidden');
      clearInterval(countdownTimer);
    });
  }

  if (confirmBtn) {
    confirmBtn.addEventListener('click', () => {
      window.location.href = markCompletedBtn.getAttribute("data-completion-url");
    });
  }

  window.addEventListener('keydown', event => {
    if (event.key === 'Escape') {
      modal.classList.add('hidden');
      clearInterval(countdownTimer);
    }
  });
})();

document.querySelectorAll("[id^='replyButton']").forEach(button => {
  button.addEventListener('click', function() {
    const commentId = this.id.split('-')[1];
    const form = document.getElementById(`replyForm-${commentId}`);
    form.classList.toggle('hidden');
  });
});
