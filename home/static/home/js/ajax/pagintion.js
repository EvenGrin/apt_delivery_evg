$(document).ready(function() {
  // Обработчик клика по ссылкам категорий
  $('a[data-category-id]').click(function(e) {
    e.preventDefault(); // Предотвращаем стандартную перезагрузку страницы
    var categoryId = $(this).data('category-id');
    // Выполняем AJAX-запрос
    $.ajax({
      url: "/ajax", // URL-адрес для AJAX-запроса
      data: { 'category': categoryId }, // Передаем ID категории
      dataType: "html", // Ожидаем HTML-ответ
      success: function(data) {
        // Обновляем div с результатами
        $('#card_inner').html(data);
      },
      error: function() {
        // Вывод сообщения об ошибке (необязательно)
        console.error('Ошибка AJAX');
      }
    });
  });
});
