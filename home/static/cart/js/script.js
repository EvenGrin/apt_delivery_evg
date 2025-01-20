$(document).ready(function() {
    const modalId = '#CreateOrderModal';
    const modalOpenKey = 'modal_open';
    const emptyCartAlert = $('.alert.alert-danger.text-center'); //находим элемент с классом
    // Функция для открытия модального окна
    function openModal() {
        $(modalId).modal('show');
        sessionStorage.setItem(modalOpenKey, 'true');
    }

    // Функция для закрытия модального окна
    function closeModal() {
        $(modalId).modal('hide');
        sessionStorage.removeItem(modalOpenKey);
    }

    // Обработчик отправки формы
    $('form.ajaxForm').on('submit', function() {
         sessionStorage.setItem(modalOpenKey, 'true'); //устанавливаем флаг перед отправкой формы
    });



    // Проверка sessionStorage при загрузке страницы и проверка корзины
     if (sessionStorage.getItem(modalOpenKey) === 'true') {
         if (emptyCartAlert.length === 0 || emptyCartAlert.css('display') === 'none' ) {
             // Если алерта нет, либо он скрыт - открываем
            openModal();
         }
        sessionStorage.removeItem(modalOpenKey);
    }


     // Закрытие модального окна
    $('#CreateOrderModal .btn-close, #CreateOrderModal [data-bs-dismiss="modal"]').on('click', function() {
        closeModal();
    });


});