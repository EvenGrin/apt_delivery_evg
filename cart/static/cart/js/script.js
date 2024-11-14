let productList = []
let cartList = []

// Функции для сохранения данных в хранилище
const saveToLocalStorage = (key, data) => {
    localStorage.setItem(key, JSON.stringify(data));
}

const getFromStorage = (key, default_) => {
    return JSON.parse(localStorage.getItem(key)) || default_;
}

// Парсинг карточек товара
const getProducts = () => {
    document.querySelectorAll('.meal-item').forEach(element => {
        const productID = element.dataset.id
        const isInCart = cartList.some(productInCart => productInCart.id === productID);

        if (isInCart) {
            element.querySelector(".meal-add-button").textContent = "Удалить из корзины"
            element.querySelector(".meal-add-button").classList.remove('btn-primary');
            element.querySelector(".meal-add-button").classList.add('btn-danger');
        }

        productList.push({
            id: productID,
            name: element.querySelector(".meal-name ").textContent,
            imageURL: element.querySelector(".meal-image").src,
            price: element.querySelector(".meal-price").textContent,
            category_name: element.querySelector(".meal-category").textContent
        })
    })
}

// Обработка событий карточки товара
const handleProductEvents = () => {
    document.querySelectorAll('.meal-item').forEach(element => {
        const productID = element.dataset.id;
        element.querySelector('.meal-add-button').addEventListener('click', event => {
            const isInCart = cartList.some(productInCart => productInCart.id === productID);

            if (isInCart) {
                event.target.classList.add('btn-primary');
                event.target.classList.remove('btn-danger');
                event.target.textContent = "В корзину"
                cartList = cartList.filter(productInCart => productInCart.id !== productID);

            } else {
                event.target.classList.remove('btn-primary');
                event.target.classList.add('btn-danger');
                event.target.textContent = "Удалить из корзины"
                const productToAdd = productList.find(productInList => productInList.id === productID);
                cartList.push(productToAdd);
            }

            saveToLocalStorage('cart', cartList)
        })
    })
}

// Функция вызова при загрузке страницы
const onLoad = () => {
    cartList = getFromStorage('cart', []);

    getProducts();
    handleProductEvents();
}

document.addEventListener("DOMContentLoaded", () => {
    onLoad();
})