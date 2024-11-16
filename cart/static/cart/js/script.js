$(".add-to-cart-button").on("click", function(e) {
    e.preventDefault();
  
    const productId = $(this).data("product-id");
    const quantity = $(this).data("quantity") || 1;
  
    $.ajax({
      type: "POST", // Важно указать POST для отправки данных
      url: "/add-to-cart/", // Путь к вашему представлению
      data: {
        product_id: productId,
        quantity: quantity
      },
      success: function(response) {
        if (response.success) {
          // Обновить отображение корзины
          updateCart(response.cart_count); // Передаем количество товаров в корзине
        } else {
          alert("Ошибка добавления товара в корзину."); // Обработка ошибок
        }
      },
      error: function(xhr, status, error) {
        console.error("AJAX error:", error);
        alert("Ошибка связи с сервером."); // Обработка ошибок
      }
  
    });
  });
  
  
  function updateCart(cartCount){
    $(".cart-count").text(cartCount);
    // ...другой код обновления корзины
  }
  
