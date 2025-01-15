$(document).ready(function () {
  function updateCart() {
    $("#head div").remove();
    $("#head").after(
      "<div class='alert alert-danger text-center'>Корзина пуста</div>"
    );
    $("div.card").remove();
    $("div.modal").remove();
  }
  $(document).on("click", ".cart_empty", function (e) {
    $.get("/cart_empty/", {}, (data) => {
      updateCart()
    });
  });
// дублирование функции
  $(document).on("click", ".cart_remove", function (e) {
    $.get("/remove_from_cart/", { meal_id: $(this).data("id") }, () => {
      if ($(".card").length - 1 == 0) {
        updateCart()
      }
      $(this).closest(".card").remove();
    });
  });

});
