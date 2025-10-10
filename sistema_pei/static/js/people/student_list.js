// Script para gerenciar tooltips de sincronização e busca/selecao de cursos na lista de alunos

document.addEventListener("DOMContentLoaded", () => {
  const sync_icons = Array.from(document.getElementsByClassName("sync_icon"));
  const sync_messages = Array.from(document.getElementsByClassName("sync_message"));

  const showSyncMessage = (messageElement, messagePosition) => {
    messageElement.style.transform = `translateY(${messagePosition}px)`;
    messageElement.style.display = "block";
  };

  const hideSyncMessage = (messageElement) => {
    messageElement.style.display = "none";
  };

  const calculateMessagePosition = (syncElement) => {
    const element_position = syncElement.getBoundingClientRect();
    return window.scrollY + element_position.top + 50;
  };

  sync_icons.forEach((element, index) => {
    const messageElement = sync_messages[index];

    element.addEventListener("mouseenter", () => {
      const message_position = calculateMessagePosition(element);
      showSyncMessage(messageElement, message_position);
    });

    element.addEventListener("mouseleave", () => {
      hideSyncMessage(messageElement);
    });
  });

  const courseSearch = document.getElementById("courseSearch");
  const courseList = document.getElementById("courseList");
  const noCourseResults = document.getElementById("noCourseResults");
  const courses = Array.from(document.querySelectorAll(".course-item"));

  if (window.studentListConfig.selectedCourseId) {
    const selectedCourseLabel = document.querySelector(
      `label[for="course_${window.studentListConfig.selectedCourseId}"]`
    );
    if (selectedCourseLabel) {
      courseSearch.value = selectedCourseLabel.textContent.trim();
    }
  }

  window.filterCourses = function () {
    const searchValue = courseSearch.value.toLowerCase();
    let hasResults = false;

    courses.forEach((course) => {
      const courseName = course.querySelector("label").textContent.toLowerCase();
      if (courseName.includes(searchValue)) {
        course.style.display = "flex";
        hasResults = true;
      } else {
        course.style.display = "none";
      }
    });

    courseList.style.display = searchValue && hasResults ? "block" : "none";
    noCourseResults.style.display = searchValue && !hasResults ? "block" : "none";
  };

  window.selectCourse = function (courseName) {
    courseSearch.value = courseName;
    courseList.style.display = "none";
  };
});
