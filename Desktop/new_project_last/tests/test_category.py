import pytest
from src.category import Category
from src.product import Product


@pytest.fixture
def product():
    return Product("Ноутбук", "Мощный", 50000, 10)


@pytest.fixture
def category(product):
    return Category("Электроника", "Техника", [product])


def test_category_init(category, product):
    assert category.name == "Электроника"
    assert category.description == "Техника"
    assert len(category.products) == 1
    assert category.products[0] == product


def test_category_name_type(category):
    assert isinstance(category.name, str)


def test_category_products_is_list(category):
    assert isinstance(category.products, list)


def test_category_count(product):
    Category.category_count = 0
    Category.product_count = 0
    
    cat1 = Category("A", "A", [product])
    cat2 = Category("B", "B", [product, product])
    
    assert Category.category_count == 2
    assert Category.product_count == 3


def test_category_empty_products():
    Category.category_count = 0
    Category.product_count = 0
    
    cat = Category("Пусто", "Нет товаров", [])
    
    assert Category.category_count == 1
    assert Category.product_count == 0
    assert len(cat.products) == 0
