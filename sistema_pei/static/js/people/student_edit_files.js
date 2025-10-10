document.addEventListener("DOMContentLoaded", function () {
  const addFilesButton = document.getElementById("add-files-button");
  const fileInput = document.querySelector("input[type='file'][id]");
  const fileListContainer = document.getElementById("file-list");

  if (addFilesButton && fileInput && fileListContainer) {
    addFilesButton.addEventListener("click", function () {
      fileInput.click();
    });

    fileInput.addEventListener("change", function (event) {
      const files = event.target.files;
      fileListContainer.innerHTML = "";
      for (let i = 0; i < files.length; i++) {
        const p = document.createElement("p");
        p.textContent = files[i].name;
        fileListContainer.appendChild(p);
      }
    });
  }
});
