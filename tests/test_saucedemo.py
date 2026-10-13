"""
Pre-entrega: login, catálogo y carrito en saucedemo.com
"""
import logging

from selenium.webdriver.support import expected_conditions as EC

from utils import locators
from utils.helpers import (
    add_first_product_to_cart,
    get_cart_count,
    get_cart_items,
    get_product_info,
    get_products,
    go_to_cart,
    load_credentials,
    login,
    wait_for,
)

log = logging.getLogger(__name__)


# ---------- Login ----------

def test_login_with_valid_user(driver):
    credentials = load_credentials()
    login(driver, credentials["username"], credentials["password"])

    assert "/inventory.html" in driver.current_url
    assert driver.find_element(*locators.APP_LOGO).text == "Swag Labs"
    assert driver.find_element(*locators.PAGE_TITLE).text == "Products"


# ---------- Catálogo ----------

def test_inventory_title(logged_driver):
    assert logged_driver.title == "Swag Labs"
    assert logged_driver.find_element(*locators.PAGE_TITLE).text == "Products"


def test_inventory_has_products(logged_driver):
    products = get_products(logged_driver)
    assert len(products) > 0, "No se encontraron productos en el inventario"

    name, price = get_product_info(products[0])
    log.info("Primer producto: %s - %s", name, price)

    assert name, "El primer producto no tiene nombre"
    assert price.startswith("$"), f"Precio con formato inesperado: {price}"


def test_inventory_ui_elements(logged_driver):
    wait = wait_for(logged_driver)

    menu = wait.until(EC.element_to_be_clickable(locators.BURGER_MENU))
    sort_filter = wait.until(EC.visibility_of_element_located(locators.SORT_FILTER))
    cart = wait.until(EC.visibility_of_element_located(locators.CART_LINK))

    assert menu.is_displayed()
    assert sort_filter.is_displayed()
    assert cart.is_displayed()


# ---------- Carrito ----------

def test_add_first_product_to_cart(logged_driver):
    assert get_cart_count(logged_driver) == 0

    name, price = add_first_product_to_cart(logged_driver)
    assert get_cart_count(logged_driver) == 1

    go_to_cart(logged_driver)
    cart_items = get_cart_items(logged_driver)

    assert len(cart_items) == 1
    assert cart_items[0] == (name, price), (
        f"En el carrito aparece {cart_items[0]} y se esperaba {(name, price)}"
    )
