// Valida seleção de matriz no formulário de disciplinas e controla modal de confirmação
document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("subject_form")
  const withoutMatrxModal = document.getElementById("WithoutMatrxConfirmModal")
  const confirmModelBtn = document.getElementById("confirmModalBtn")
  const cancelModalBtn = document.getElementById("cancelModalBtn")
  const matrixArray = Array.from(document.getElementsByClassName("matrix_checkbox"))

  if (!form) return

  form.addEventListener("submit", (e) => { FormSubmit(e, form) })
  cancelModalBtn?.addEventListener('click', () => { withoutMatrxModal.classList.add("hidden") })
  confirmModelBtn?.addEventListener('click', () => { form.submit() })

  function FormSubmit(event, form) {
    event.preventDefault()
    let hasMatrixSelected = false

    matrixArray.forEach(element => { if (element.checked) hasMatrixSelected = true })

    !hasMatrixSelected && matrixArray.length > 0
      ? withoutMatrxModal.classList.remove('hidden')
      : form.submit()
  }

  window.RadioEfect = function(elementsClass, elementCheckedId) {
    const Elements = Array.from(document.getElementsByClassName(elementsClass))
    Elements.forEach(element => { if (element.id != elementCheckedId) element.checked = false })
  }
})
