document.addEventListener('DOMContentLoaded', function() {
  const courseSelect = document.getElementById('id_course');
  const subjectSelect = document.getElementById('id_subject');

  subjectSelect.disabled = true;
  subjectSelect.innerHTML = '<option value="default" selected disabled>Selecione o curso primeiro...</option>';

  if (courseSelect.value !== 'default') {
      subjectSelect.disabled = false;
      fetch(`/academics/offers/get_subjects_by_course_id/${courseSelect.value}/`)
          .then(response => response.json())
          .then(data => {
              subjectSelect.innerHTML = '<option value="default" selected disabled>Selecione a disciplina...</option>';
              data.subjects.forEach(subject => {
                  const option = document.createElement('option');
                  option.value = subject.id;
                  option.textContent = subject.name;
                  subjectSelect.appendChild(option);
              });
              if (subjectSelect.dataset.selectedValue) {
                  subjectSelect.value = subjectSelect.dataset.selectedValue;
              }
          });
  }

  courseSelect.addEventListener('change', function() {
      const courseId = this.value;
      if (courseId !== 'default') {
          subjectSelect.disabled = false;
          subjectSelect.innerHTML = '<option value="default" selected disabled>Selecione a disciplina...</option>';

          fetch(`/academics/offers/get_subjects_by_course_id/${courseId}/`)
              .then(response => response.json())
              .then(data => {
                  subjectSelect.innerHTML = '<option value="default" selected disabled>Selecione a disciplina...</option>';
                  data.subjects.forEach(subject => {
                      const option = document.createElement('option');
                      option.value = subject.id;
                      option.textContent = subject.name;
                      subjectSelect.appendChild(option);
                  });
              });
      } else {
          subjectSelect.disabled = true;
          subjectSelect.innerHTML = '<option value="default" selected disabled>Selecione a disciplina...</option>';
      }
  });
});
