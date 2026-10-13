"""
Selectores de saucedemo.com agrupados por página.

Prefiero tenerlos en un solo lugar: si cambia el HTML del sitio,
se corrige acá y no en cada test.
"""
from selenium.webdriver.common.by import By

# --- Login ---
USERNAME_INPUT = (By.ID, "user-name")
PASSWORD_INPUT = (By.ID, "password")
LOGIN_BUTTON = (By.ID, "login-button")

# --- Inventario ---
APP_LOGO = (By.CLASS_NAME, "app_logo")            # texto "Swag Labs"
PAGE_TITLE = (By.CSS_SELECTOR, "span.title")      # texto "Products"
BURGER_MENU = (By.ID, "react-burger-menu-btn")
SORT_FILTER = (By.CSS_SELECTOR, "[data-test='product-sort-container']")
INVENTORY_ITEM = (By.CLASS_NAME, "inventory_item")
ITEM_NAME = (By.CLASS_NAME, "inventory_item_name")
ITEM_PRICE = (By.CLASS_NAME, "inventory_item_price")
ADD_TO_CART_BUTTON = (By.CSS_SELECTOR, "button[id^='add-to-cart']")
CART_LINK = (By.CLASS_NAME, "shopping_cart_link")
CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")

# --- Carrito ---
CART_ITEM = (By.CLASS_NAME, "cart_item")
