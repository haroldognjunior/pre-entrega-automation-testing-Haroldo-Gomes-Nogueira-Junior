"""
Funciones auxiliares para los tests de saucedemo.com.

La idea es que los tests lean como pasos ("login", "agregar producto",
"ir al carrito") y que el detalle de Selenium quede acá.
"""
import json
import logging
import os
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from utils import locators

BASE_URL = "https://www.saucedemo.com/"
DEFAULT_TIMEOUT = 10
CREDENTIALS_FILE = Path(__file__).parent.parent / "datos" / "usuarios.json"

log = logging.getLogger(__name__)


def create_driver():
    """Crea una instancia de Chrome. Con HEADLESS=1 corre sin ventana."""
    options = webdriver.ChromeOptions()
    options.add_argument("--window-size=1366,900")

    # Chrome muestra un aviso de "contraseña filtrada" con secret_sauce
    # y tapa la página; con esto se desactiva.
    options.add_experimental_option("prefs", {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.password_manager_leak_detection": False,
    })

    if os.getenv("HEADLESS") == "1":
        options.add_argument("--headless=new")

    # Desde Selenium 4.6 no hace falta descargar chromedriver a mano
    return webdriver.Chrome(options=options)


def wait_for(driver, timeout=DEFAULT_TIMEOUT):
    return WebDriverWait(driver, timeout)


def load_credentials(user_key="standard"):
    with open(CREDENTIALS_FILE, encoding="utf-8") as file:
        return json.load(file)[user_key]


def login(driver, username, password):
    """Hace login y espera (explícitamente) a que cargue el inventario."""
    driver.get(BASE_URL)
    wait_for(driver).until(EC.visibility_of_element_located(locators.USERNAME_INPUT))

    driver.find_element(*locators.USERNAME_INPUT).send_keys(username)
    driver.find_element(*locators.PASSWORD_INPUT).send_keys(password)
    driver.find_element(*locators.LOGIN_BUTTON).click()

    wait_for(driver).until(EC.url_contains("/inventory.html"))
    log.info("Login OK con '%s'", username)


def get_products(driver):
    return wait_for(driver).until(
        EC.visibility_of_all_elements_located(locators.INVENTORY_ITEM)
    )


def get_product_info(product):
    """Devuelve (nombre, precio) de un producto del inventario o del carrito."""
    name = product.find_element(*locators.ITEM_NAME).text
    price = product.find_element(*locators.ITEM_PRICE).text
    return name, price


def get_cart_count(driver):
    # El badge no existe cuando el carrito está vacío
    badges = driver.find_elements(*locators.CART_BADGE)
    return int(badges[0].text) if badges else 0


def add_first_product_to_cart(driver):
    """Agrega el primer producto y devuelve su (nombre, precio)."""
    first_product = get_products(driver)[0]
    name, price = get_product_info(first_product)

    first_product.find_element(*locators.ADD_TO_CART_BUTTON).click()
    wait_for(driver).until(EC.visibility_of_element_located(locators.CART_BADGE))

    log.info("Agregado al carrito: %s (%s)", name, price)
    return name, price


def go_to_cart(driver):
    driver.find_element(*locators.CART_LINK).click()
    wait_for(driver).until(EC.url_contains("/cart.html"))


def get_cart_items(driver):
    items = wait_for(driver).until(
        EC.visibility_of_all_elements_located(locators.CART_ITEM)
    )
    return [get_product_info(item) for item in items]
