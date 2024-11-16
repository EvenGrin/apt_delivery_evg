$(".add-to-cart-button").on("click", function(e) {
    e.preventDefault();

    const productId = $(this).closest(".meal-item").data("id");
    const quantity = $(this).data("quantity") || 1;

    $.ajax({
        type: "GET",
        url: "/add-to-cart/",
        data: {
            meal_id: productId,
            quantity: quantity
        },
        success: function(response) {
            if (response.success) {
            } else {
                alert("Ошибка добавления товара в корзину.");
            }
        },
        error: function(xhr, status, error) {
            console.error("AJAX error:", error);
            alert("Ошибка связи с сервером.");
        }
    });
});

