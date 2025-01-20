$(document).ready(function () {

    $(document).on("click", ".take_order", function (e) {
    $.get("/deliver/take_order/", { order_id:  $(this).data("id")}, (data) => {

            // Обновляем кнопки только если элемент (кнопка) передан
            $(this).html(data.message).addClass('btn-outline-primary').removeClass('btn-primary')

        });

    });


    })