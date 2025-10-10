//Busca por discente no input de inclusão em oferta
document.addEventListener("DOMContentLoaded", () => {
  const searchInput = document.getElementById("studentSearch");
  const students = document.querySelectorAll(".student-item");
  const studentList = document.getElementById("studentList");
  const noResultsMessage = document.getElementById("noResultsMessage");

  searchInput.addEventListener("input", () => {
    const searchValue = searchInput.value.toLowerCase();
    let hasResults = false;

    students.forEach(student => {
      const studentName = student.querySelector(".student-name").textContent.toLowerCase();
      if (studentName.includes(searchValue)) {
        student.style.display = "flex";
        hasResults = true;
      } else {
        student.style.display = "none";
      }
    });

    noResultsMessage.style.display = hasResults ? "none" : "block";
    studentList.style.display = searchValue && hasResults ? "block" : "none";
  });
});
