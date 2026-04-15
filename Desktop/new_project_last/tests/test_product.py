import pytest
from src.product import Product


@pytest.fixture
def product():
    return Product("Ноутбук", "Мощный", 50000, 10)


def test_product_init(product):
    assert product.name == "Ноутбук"
    assert product.description == "Мощный"
    assert product.price == 50000
    assert product.quantity == 10


def test_product_name_type(product):
    assert isinstance(product.name, str)


def test_product_price_type(product):
    assert isinstance(product.price, (int, float))


def test_product_quantity_type(product):
    assert isinstance(product.quantity, int)
