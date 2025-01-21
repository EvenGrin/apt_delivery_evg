$(document).ready(function () {

    $(document).on("click", ".take_order", function (e) {
    $.get("/deliver/take_order/", { order_id:  $(this).data("id")}, (data) => {
    console.log(data.count)
            $('#count').html(data.count)
            // Обновляем кнопки только если элемент (кнопка) передан
            $(this).html(data.message).addClass('btn-outline-primary').removeClass('btn-primary')
        });
    });

    $(document).on("click", ".in_way, .delivered", function (e) {
    $.get("/deliver/update_status/", { order_id:  $(this).data("id")}, (data) => {
            console.log($(this))
            $(this).html(data.message).addClass(data.class_add).removeClass(data.class_remove)
        });
    });

    })