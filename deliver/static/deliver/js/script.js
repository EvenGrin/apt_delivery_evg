$(document).ready(function () {
    function updateData(data, mealId=0){
            $('.cart_info').html(data.cart_count ? data.cart_count : '');
            $('#total_price').html(data.total_price);
            $('#amount').html(data.amount); // Обновляем #amount
            if (mealId) {
                $(`.card[data-id='${mealId}']`).find('.total_amount').html(data.total_amount);
            }
    }
    $(document).on("click", ".take_order", function (e) {
        updateDataCart("deliver/take/", $(this).data("id"), $(this));
    });

//    $(document).on("click", ".sub-from-cart-button", function (e) {
//        updateDataCart("deliver/sub/", $(this).data("id"), $(this));
//    });
//
//    $(document).on("click", ".cart_empty", function (e) {
//        $.get("/cart_empty/", {}, (data) => {
//            updateData(data)
//            updateCart()
//        });
//    });
    })