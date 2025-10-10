//Atualiza labels ao incluir planilha de importação de dados
function updateUploadLabel() {
    const input = document.getElementById('file-upload');
    const label = document.getElementById('upload-label');
    const div = document.getElementById('upload-div');

    if (input.files && input.files.length > 0) {
    label.textContent = "✅ Planilha adicionada";
    div.classList.remove('hover:bg-green-600', 'hover:text-white', 'cursor-pointer');
    } else {
    label.textContent = "Enviar planilha preenchida";
    div.classList.add('hover:bg-green-600', 'hover:text-white', 'cursor-pointer');
    }
}