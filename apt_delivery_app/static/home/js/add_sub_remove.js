// в шаблоне пути
$(document).ready(function () {
  function updateData(data, meal_id = 0) {
    $(".cart_info").html(data.cart_count ? data.cart_count : "");
    $("#total_price").html(data.total_price);
    $("#amount").html(data.amount); // Обновляем #amount
    if (meal_id) {
      $(`.card[data-id='${meal_id}']`)
        .find(".total_amount")
        .html(data.total_amount);
    }
  }
  function updateDataCart(url, obj, element) {
    console.log(obj);
    $.post(url, obj, (data) => {
      updateData(data, obj.meal_id);
      // Обновляем кнопки только если элемент (кнопка) передан
      if (element) {
        element.closest(".card-button").html(
          `
          <button class='cart_remove btn btn-danger  me-auto' data-id='${obj.meal_id}' data-order-id='${obj.order_id}'>Убрать</button>
          <button class="btn btn-primary sub-from-cart-button" data-id="${obj.meal_id}" data-order-id='${obj.order_id}'>-</button>
          <span>${data.quantity}</span>
          <button class="add-to-cart-button btn btn-primary cart_add" data-id="${obj.meal_id}" data-order-id='${obj.order_id}'>+</button>
          `
        );
      }
    });
  }
  function updateCart() {
    $("#head").after(
      "<div class='alert alert-danger text-center'>Корзина пуста</div>"
    );
    $("div.card").remove();
    $("div.modal").remove();
    $("#cart_buttons").remove();
  }
  $(document).on("click", ".add-to-cart-button", function (e) {
    updateDataCart(
      url_add,
      { meal_id: $(this).data("id"), order_id: $(this).data("order-id") },
      $(this)
    );
  });

  $(document).on("click", ".sub-from-cart-button", function (e) {
    updateDataCart(
      url_sub,
      { meal_id: $(this).data("id"), order_id: $(this).data("order-id") },
      $(this)
    );
  });
  $(document).on("click", ".cart_empty", function (e) {
    $.get("/cart_empty/", {}, (data) => {
      updateData(data);
      updateCart();
    });
  });
  $(document).on("click", ".cart_remove", function (e) {
    meal_id = $(this).data("id");
    order_id = $(this).data("order-id");
    $.post(url_remove, { meal_id: meal_id, order_id: order_id }, (data) => {
      updateData(data, meal_id);
      if (window.location.href.includes("cart")) {
        if ($(".card").length - 1 == 0) {
          updateCart();
        }
        $(this).closest(".card").remove();
      }
      $(this)
        .closest(".card-button")
        .html(
          "<button class='add-to-cart-button btn btn-primary cart_add ms-auto' data-id=" +
            $(this).data("id") +
            ">В корзину</button>"
        );
    });
  });
});
