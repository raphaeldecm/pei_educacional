document.addEventListener('DOMContentLoaded', function() {
  const durationSelect = document.getElementById(window.courseFormConfig.durationId);
  const periodsLabel = document.getElementById('periods-label');
  const periodsInput = document.getElementById(window.courseFormConfig.periodsId);

  function updatePeriodsLabelAndValue() {
    const selectedValue = durationSelect.value;
    if (selectedValue === 'SEMESTER') {
      periodsLabel.textContent = 'Qtd. de Semestres:';
      periodsInput.value = 7;
    } else if (selectedValue === 'YEAR') {
      periodsLabel.textContent = 'Qtd. de Anos:';
      periodsInput.value = 4;
    } else {
      periodsLabel.textContent = 'Qtd. Períodos:';
      periodsInput.value = '';
    }
  }

  updatePeriodsLabelAndValue();
  durationSelect.addEventListener('change', updatePeriodsLabelAndValue);
});
