"""
Fixtures compartidas por todos los tests.

Cada test recibe su propio navegador, así la falla de uno no
arrastra a los demás.
"""
from datetime import datetime
from pathlib import Path

import pytest

from utils.helpers import create_driver, load_credentials, login

SCREENSHOTS_DIR = Path(__file__).parent.parent / "reports" / "screenshots"


@pytest.fixture
def driver():
    browser = create_driver()
    yield browser
    browser.quit()


@pytest.fixture
def logged_driver(driver):
    """Navegador que ya pasó por el login, para los tests de catálogo y carrito."""
    credentials = load_credentials()
    login(driver, credentials["username"], credentials["password"])
    return driver


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Si un test falla, guarda una captura de pantalla en reports/screenshots."""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        browser = item.funcargs.get("driver")
        if browser is None:
            return
        SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = SCREENSHOTS_DIR / f"{item.name}_{timestamp}.png"
        browser.save_screenshot(str(file_path))
        print(f"Captura guardada en {file_path}")
