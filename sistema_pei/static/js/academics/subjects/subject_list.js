// Mostra mensagens ao passar o mouse sobre os ícones de status do preenchimento
document.addEventListener("DOMContentLoaded", () => {
  const filled_icons = Array.from(document.getElementsByClassName("filled_icon"));
  const filled_messages = Array.from(document.getElementsByClassName("filled_message"));

  const CalculateMessagePosition = (element, margin_top = 0) => {
    const element_position = element.getBoundingClientRect();
    return window.scrollY + element_position.top + margin_top;
  };

  const ShowMessage = (message_element, position) => {
    message_element.style.transform = `translateY(${position}px)`;
    message_element.style.display = 'block';
  };

  const HiddenMessage = (message_element) => {
    message_element.style.display = 'none';
  };

  filled_icons.forEach((element, index) => {
    const element_filled_message = filled_messages[index];

    element.addEventListener('mouseenter', () => {
      const filled_message_position = CalculateMessagePosition(element, 50);
      ShowMessage(element_filled_message, filled_message_position);
    });

    element.addEventListener('mouseleave', () => {
      HiddenMessage(element_filled_message);
    });
  });
});
