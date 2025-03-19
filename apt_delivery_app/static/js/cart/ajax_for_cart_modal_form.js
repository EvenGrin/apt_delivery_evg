// $(document).ready(function () {
//   const modalId = "#CreateOrderModal";
//   const modalOpenKey = "modal_open";
//   const emptyCartAlert = $(".alert.alert-danger.text-center"); //находим элемент с классом
//   // Обработчик отправки формы
//   $("form.ajaxForm").on("submit", function () {
//     sessionStorage.setItem(modalOpenKey, "true"); //устанавливаем флаг перед отправкой формы
//   });
//   // Проверка sessionStorage при загрузке страницы и проверка корзины
//   if (sessionStorage.getItem(modalOpenKey) === "true") {
//     if (
//       emptyCartAlert.length === 0 ||
//       emptyCartAlert.css("display") === "none"
//     ) {
//       // Если алерта нет, либо он скрыт - открываем
//       $(modalId).modal("show");
//       sessionStorage.setItem(modalOpenKey, "true");
//     }
//     sessionStorage.removeItem(modalOpenKey);
//   }
//   // Закрытие модального окна
//   $(
//     '#CreateOrderModal .btn-close, #CreateOrderModal [data-bs-dismiss="modal"]'
//   ).on("click", function () {
//     $(modalId).modal("hide");
//     sessionStorage.removeItem(modalOpenKey);
//   });
// });
/// <reference path="../home/jquery-3.7.1.js" />
$(document).ready(function () {
  $("form.ajaxForm").on("submit", function (ev) {
    console.log($("form.ajaxForm").serialize)
    ev.preventDefault()
    $.ajax({
      url: $(this).attr("action"),
      type: "post",
      headers: { "X-CSRFToken": '{{csrf_token}}' },
      data: $(this).serialize(),
      success: function(response) {
        console.log(response);
        if(response.url){
          window.location = response.url
        }
        // response is form in html format
        $("#formdiv").html(response);
        stylizeForm()

      }
  })
  });
});
