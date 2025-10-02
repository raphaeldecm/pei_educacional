// Preview da imagem de perfil
function previewImage(event) {
  const input = event.target;
  const file = input.files[0];
  const reader = new FileReader();

  reader.onload = function (e) {
    const preview = document.getElementById("profileImage");
    preview.src = e.target.result;
  };

  if (file) {
    reader.readAsDataURL(file);
  }
}

document.addEventListener("DOMContentLoaded", () => {
  /*
    Comportamento dos campos de anexo.
    Lista os arquivos selecionados e os adicionam ao input oculto.
  */

  const fileUpload = {
    fileList: document.getElementById("file-list"),
    inputElement: document.getElementById(window.studentFormConfig.filesInputId),
    files: [],

    init() {
      document.getElementById("add-files-button").addEventListener("click", () => {
        this.inputElement.click();
      });

      this.inputElement.addEventListener("change", (event) => {
        this.handleFileSelect(event);
      });
    },

    handleFileSelect(event) {
      const newFiles = Array.from(event.target.files);
      this.files = this.files.concat(newFiles);
      this.updateFileList();
      this.updateInputFiles();
    },

    removeFile(index) {
      this.files.splice(index, 1);
      this.updateFileList();
      this.updateInputFiles();
    },

    updateFileList() {
      this.fileList.innerHTML = "";
      this.files.forEach((file, index) => {
        const fileItem = document.createElement("div");
        fileItem.className =
          "flex justify-between gap-2 bg-transparent font-sans appearance-none border rounded w-full py-6 px-3 placeholder:font-light font-light placeholder:text-slate-500 text-slate-900 hover:border-green-500 focus:outline-green-500";

        fileItem.innerHTML = `
          <span class="flex gap-2 text-gray-700">
            <img src="${window.studentFormConfig.clipIconUrl}" alt="ícone de arquivo anexado" />
            ${file.name}
          </span>
          <button class="ml-4 text-red-500 cursor-pointer hover:underline" type="button" data-index="${index}">Remover</button>
        `;

        // Adiciona listener ao botão
        fileItem.querySelector("button").addEventListener("click", () => this.removeFile(index));

        this.fileList.appendChild(fileItem);
      });
    },

    updateInputFiles() {
      const dataTransfer = new DataTransfer();
      this.files.forEach((file) => dataTransfer.items.add(file));
      this.inputElement.files = dataTransfer.files;
    },
  };

  fileUpload.init();
  window.fileUpload = fileUpload;
});
