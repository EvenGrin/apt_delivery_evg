$(document).ready(function () {
    function updateCart(url, mealId, element) {
        $.get(url, { meal_id: mealId }, (data) => {
            $('.cart_info').html(data.cart_count ? data.cart_count : '');
            $(`.card[data-id='${mealId}']`).find('.total_amount').html(data.total_amount);
            $('#total_price').html(data.total_price);
            $('#amount').html(data.amount); // Обновляем #amount

            // Обновляем кнопки только если элемент (кнопка) передан
            if (element) {
                element.closest(".card-button").html(`
            <button class='cart_remove btn btn-danger  me-auto' data-id='${mealId}'>Убрать</button>
            <button class="btn btn-primary sub-from-cart-button" data-id="${mealId}">-</button>
            <span>${data.quantity}</span>
            <button class="add-to-cart-button btn btn-primary cart_add" data-id="${mealId}">+</button>
            `);
            }

        });
    }

    $(document).on("click", ".add-to-cart-button", function (e) {
        updateCart("/add-to-cart/", $(this).data("id"), $(this));
    });

    $(document).on("click", ".sub-from-cart-button", function (e) {
        updateCart("/sub-from-cart/", $(this).data("id"), $(this));
    });
    if (!window.location.href.includes('cart')){
    console.log(123)
    $(document).on("click", ".cart_remove", function (e) {
        updateCart("/remove_from_cart/", $(this).data("id"));
        $.get("/remove_from_cart/", { meal_id: $(this).data("id") }, (data) => {
            $(this).closest(".card-button").html("<button class='add-to-cart-button btn btn-primary cart_add ms-auto' data-id=" + $(this).data("id") + ">В корзину</button>");
        });
    });
    }

});
