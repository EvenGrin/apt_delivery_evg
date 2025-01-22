$(document).ready(function () {

    $(document).on("click", ".take_order", function (e) {
        $.get("/deliver/take_order/", { order_id: $(this).data("id") }, (data) => {
            console.log(data.count)
            $('#count').html(data.count)
            // Обновляем кнопки только если элемент (кнопка) передан
            $(this).html(data.message).addClass('btn-outline-primary').removeClass('btn-primary')

        });
    });

    $(document).on("click", ".in_way, .delivered", function (e) {
        $.get("/deliver/update_status/", { order_id: $(this).data("id") }, (data) => {
        console.log(data)
            if (!jQuery.isEmptyObject(data)) {
                id = $(this).data("id")
                console.log($(this))
                $(this).html(data.html).addClass(data.class_add).removeClass(data.class_remove)
                $(`span[data-id = "${id}"]`).html(data.status.status__name)
                if (data.status.status__id == 7) {
                $(`span[data-id = "${id}"]`).parent().addClass('btn-success').removeClass('btn-outline-primary')
                }
                console.log(data.status.status__name)

            }

        });
    });

})