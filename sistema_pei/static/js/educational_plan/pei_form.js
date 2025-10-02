// Controla comportamento das abas do PEI
document.addEventListener('DOMContentLoaded', function() {
  const peiEditContainer = document.getElementById('pei_edit_container');
  const behaviorUnSupportedNavigators = ['firefox'];

  function isNavigatorSupported(unsupportedList) {
    const userAgent = navigator.userAgent.toLowerCase();
    return !unsupportedList.some(navigator => userAgent.includes(navigator));
  }

  function scrollToElement(element) {
    if (!element) return;

    const top = element.getBoundingClientRect().top + (window.pageYOffset || window.scrollY || 0);
    if (isNavigatorSupported(behaviorUnSupportedNavigators)) {
      window.scrollTo({ top: top, behavior: 'smooth' });
    } else {
      window.scrollTo({ top: top });
    }
  }

  function showTab(tab) {
    if (!peiEditContainer) return;

    scrollToElement(peiEditContainer);

    document.querySelectorAll('.tab-content').forEach(content => {
      content.classList.add('hidden');
    });

    document.querySelectorAll('nav ul li').forEach(tabItem => {
      tabItem.classList.remove('active');
    });

    const activeContent = document.getElementById(`content-${tab}`);
    if (activeContent) {
      activeContent.classList.remove('hidden');
    }
  }


  window.showTab = showTab;

  document.querySelectorAll('nav ul li[data-tab]').forEach(li => {
    li.addEventListener('click', function () {
      const tab = li.getAttribute('data-tab');
      if (tab) showTab(tab);
    });
  });

  showTab('metodologia');
});
