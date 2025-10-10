// Script para gerenciar modais, preview de imagem e anexos no perfil do aluno

document.addEventListener('DOMContentLoaded', () => {
  // Modal de confirmação
  const updateForm = document.getElementById('updateForm');
  const submitButton = document.getElementById('submit-button');
  const modal = document.getElementById('confirmationModal');
  const confirmButton = document.getElementById('confirmButton');
  const cancelButton = document.getElementById('cancelButton');

  submitButton.addEventListener('click', (event) => {
    event.preventDefault();
    modal.classList.remove('hidden');
  });

  confirmButton.addEventListener('click', () => {
    modal.classList.add('hidden');
    updateForm.submit();
  });

  cancelButton.addEventListener('click', () => {
    modal.classList.add('hidden');
  });

  // Preview de imagem
  window.previewImage = function(event) {
    const input = event.target;
    const file = input.files[0];
    const reader = new FileReader();

    reader.onload = function(e) {
      const preview = document.getElementById('profileImage');
      preview.src = e.target.result;
    };

    if (file) reader.readAsDataURL(file);
  };

  // Gerenciamento de anexos
  const fileUpload = {
    fileList: document.getElementById('file-list'),
    inputElement: document.getElementById('{{ form.files.id_for_label }}'),
    files: [],

    init() {
      document.getElementById('add-files-button').addEventListener('click', () => {
        this.inputElement.click();
      });

      this.inputElement.addEventListener('change', (event) => this.handleFileSelect(event));
    },

    handleFileSelect(event) {
      this.files = this.files.concat(Array.from(event.target.files));
      this.updateFileList();
      this.updateInputFiles();
    },

    removeFile(index) {
      this.files.splice(index, 1);
      this.updateFileList();
      this.updateInputFiles();
    },

    updateFileList() {
      this.fileList.innerHTML = '';
      this.files.forEach((file, index) => {
        const fileItem = document.createElement('div');
        fileItem.className = 'flex justify-between gap-2 bg-transparent truncate font-poppins appearance-none border rounded w-full py-6 px-3 placeholder:font-light font-light placeholder:text-slate-500 text-slate-900 hover:border-green-500 focus:outline-green-500';
        fileItem.innerHTML = `
          <span class="flex gap-2 text-gray-700">
            <img src="{% static 'images/icons/clip_icon.svg' %}" alt="icone de clip de papel" />
            ${file.name}
          </span>
          <button class="ml-4 text-red-500 cursor-pointer hover:underline" onclick="fileUpload.removeFile(${index})">Remover</button>
        `;
        this.fileList.appendChild(fileItem);
      });
    },

    updateInputFiles() {
      const dataTransfer = new DataTransfer();
      this.files.forEach(file => dataTransfer.items.add(file));
      this.inputElement.files = dataTransfer.files;
    }
  };

  fileUpload.init();
  window.fileUpload = fileUpload;

  // Modal de confirmação para remover arquivos
  const removeButtons = document.querySelectorAll('.removeFile');
  let formToSubmit;

  removeButtons.forEach(button => {
    button.addEventListener('click', (event) => {
      event.preventDefault();
      formToSubmit = button.closest('form');
      modal.classList.remove('hidden');
    });
  });

  cancelButton.addEventListener('click', () => {
    modal.classList.add('hidden');
  });

  confirmButton.addEventListener('click', () => {
    if (formToSubmit) formToSubmit.submit();
    modal.classList.add('hidden');
  });
});
