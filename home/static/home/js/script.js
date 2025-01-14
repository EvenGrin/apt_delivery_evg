$(document).ready(function () {
  $(document).on("click", ".add-to-cart-button", function (e) {
    $.get("/add-to-cart/", { meal_id: $(this).data("id") }, (data) => {
      $('.cart_info').html(data.cart_count? data.cart_count: '')
      console.log($(this).closest('span.total_amount'))
      $(this)
        .closest(".card-button")
        .html(
        `
          <button class='cart_remove btn btn-danger  me-auto' data-id='${$(this).data("id")}'>Убрать</button>
          <button class="btn btn-primary sub-from-cart-button" data-id="${$(this).data("id")}">-</button>
          <span>${data.quantity}</span>
          <button class="add-to-cart-button btn btn-primary cart_add" data-id="${$(this).data("id")}">+</button>
        `
        );
    });
  });

  $(document).on("click", ".sub-from-cart-button", function (e) {
    $.get("/sub-from-cart/", { meal_id: $(this).data("id") }, (data) => {
      $('.cart_info').html(data.cart_count? data.cart_count: '')
      $(this)
        .closest(".card-button")
        .html(
        `
          <button class='cart_remove btn btn-danger  me-auto' data-id='${$(this).data("id")}'>Убрать</button>
          <button class="btn btn-primary sub-from-cart-button" data-id="${$(this).data("id")}">-</button>
          <span>${data.quantity}</span>
          <button class="add-to-cart-button btn btn-primary cart_add" data-id="${$(this).data("id")}">+</button>
        `
        );
    });
  });

  $(document).on("click", ".cart_remove", function (e) {

    $.get("/remove_from_cart/", { meal_id: $(this).data("id") }, (data) => {
      $(this).closest(".card-button").html("<button class='add-to-cart-button btn btn-primary cart_add ms-auto' data-id="+ $(this).data("id") +">В корзину</button>");
      $('.cart_info').html(data.cart_count? data.cart_count: '')
    });
  });
});
