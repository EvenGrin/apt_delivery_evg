$(document).ready(function () {
  $(document).on("click", ".cart_empty", function (e) {
    $.get("/cart_empty/", {}, (data) => {
      $("#head div").remove();
      $("#head").after(
        "<div class='alert alert-danger text-center'>Корзина пуста</div>"
      );
      $("div.card").remove();
      $("div.modal").remove();
    });
  });

  $(document).on("click", ".cart_remove", function (e) {
    console.log($(this).closest(".card"));
    $.get("/remove_from_cart/", { meal_id: $(this).data("id") }, () => {
      if ($(".card").length-1 == 0) {
        $("#head div").remove();
        $("#head").after(
          "<div class='alert alert-danger text-center'>Корзина пуста</div>"
        );
        $("div.card").remove();
        $("div.modal").remove();
      }
      $(this).closest(".card").remove();
    });
  });
});
