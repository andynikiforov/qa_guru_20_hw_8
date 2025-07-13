"""
Протестируйте классы из модуля homework/models.py
"""
import pytest

from tests.models import Product
from tests.models import Cart


@pytest.fixture
def product():
    return Product("book", 100, "This is a book", 1000)

@pytest.fixture
def cart():
    return Cart()


@pytest.fixture
def product_1():
    return Product("book", 100, "This is another book", 10)

@pytest.fixture
def product_2():
    return Product("pen", 20, "This is a Pen", 5)


class TestProducts:
    """
    Тестовый класс - это способ группировки ваших тестов по какой-то тематике
    Например, текущий класс группирует тесты на класс Product
    """

    def test_product_check_quantity(self, product):
        # TODO напишите проверки на метод check_quantity
        assert product.check_quantity(1000) is True
        assert product.check_quantity(999) is True
        assert product.check_quantity(1001) is False

    def test_product_buy(self, product):
        # TODO напишите проверки на метод buy
        product.buy(999)
        assert product.quantity == 1


    def test_product_buy_more_than_available(self, product):
        # TODO напишите проверки на метод buy,
        #  которые ожидают ошибку ValueError при попытке купить больше, чем есть в наличии
        with pytest.raises(ValueError):
            product.buy(1001)


class TestCart:
    """
    TODO Напишите тесты на методы класса Cart
        На каждый метод у вас должен получиться отдельный тест
        На некоторые методы у вас может быть несколько тестов.
        Например, негативные тесты, ожидающие ошибку (используйте pytest.raises, чтобы проверить это)
    """
    def test_add_product_cart(self, cart, product_1, product_2):
        cart.add_product(product_1, 3) # Добавление товара в пустую корзину
        assert cart.products[product_1] == 3

        cart.add_product(product_1, 2) # Добавление такого же товара
        assert cart.products[product_1] == 5

        cart.add_product(product_2, 2) # Добавление другого товара в непустую корзину
        assert cart.products == {product_1 : 5, product_2 : 2}

    def test_remove_product(self, cart, product_1, product_2):
        cart.add_product(product_1, 5)
        cart.add_product(product_2, 2)

        cart.remove_product(product_1, 3) # Удаляем валидное количество товара
        assert cart.products[product_1] == 2

        cart.remove_product(product_2, 5)  # Удаляем больше, чем есть товара
        assert product_2 not in cart.products

        cart.remove_product(product_1) # Удаляем без передачи количества товара
        assert product_1 not in cart.products

    def test_clear(self, cart, product_1, product_2):
        cart.add_product(product_1, 5)
        cart.add_product(product_2, 2)

        cart.clear()
        assert cart.products == {}

    def test_get_total_price(self, cart, product_1, product_2):
        cart.add_product(product_1)
        assert cart.get_total_price() == 100

    def test_buy(self, cart, product_1, product_2):
        cart.add_product(product_1, 5)
        cart.add_product(product_2, 2)

        cart.buy()

        assert len(cart.products) == 0
        assert product_1.quantity == 5
        assert product_2.quantity == 3

    def test_buy_fail(self, cart, product_1, product_2):
        cart.add_product(product_1, 11)
        with pytest.raises(ValueError):
            cart.buy()
