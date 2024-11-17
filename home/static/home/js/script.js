$(document).ready(function () {
  $(document).on("click", ".add-to-cart-button", function (e) {
    $.get("/add-to-cart/", { meal_id: $(this).data("id") }, (data) => {
      $(this)
        .closest(".card-button")
        .html(
          "<button class='cart_remove btn btn-danger  me-auto' data-id='" +
            $(this).data("id") +
            "'>Убрать</button>"
        );
    });
  });

  $(document).on("click", ".cart_remove", function (e) {
    console.log($(this));
    $.get("/remove_from_cart/", { meal_id: $(this).data("id") }, () => {
      $(this).closest(".card-button").html("<button class='add-to-cart-button btn btn-primary cart_add ms-auto' data-id="+ $(this).data("id") +">В корзину</button>");
    });
  });
});
