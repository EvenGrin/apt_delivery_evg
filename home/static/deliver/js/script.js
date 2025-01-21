$(document).ready(function () {

    $(document).on("click", ".take_order", function (e) {
    $.get("/deliver/take_order/", { order_id:  $(this).data("id")}, (data) => {
    console.log(data.count)
            $('#count').html(data.count)
            // Обновляем кнопки только если элемент (кнопка) передан
            $(this).html(data.message).addClass('btn-outline-primary').removeClass('btn-primary')
        });
    });

    $(document).on("click", ".in_way", function (e) {
    console.log(123)
    $.get("/deliver/update_status/", { order_id:  $(this).data("id")}, (data) => {
            $(this).html('Изменить на доставлен').addClass('delivered').removeClass('in_way')
        });
    });

    })