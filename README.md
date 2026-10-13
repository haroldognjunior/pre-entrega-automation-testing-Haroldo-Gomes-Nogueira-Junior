# Pre-entrega Automation Testing – Haroldo Nogueira

Automatización de pruebas sobre [saucedemo.com](https://www.saucedemo.com) con Python, Selenium WebDriver y Pytest.

## Qué se prueba

| Área | Test | Qué valida |
|---|---|---|
| Login | `test_login_with_valid_user` | Login con `standard_user`, redirección a `/inventory.html`, textos "Swag Labs" y "Products" |
| Catálogo | `test_inventory_title` | Título de la pestaña y de la sección |
| Catálogo | `test_inventory_has_products` | Hay productos visibles; registra nombre y precio del primero |
| Catálogo | `test_inventory_ui_elements` | Menú, filtro de orden y carrito presentes |
| Carrito | `test_add_first_product_to_cart` | Agrega el primer producto, el contador pasa a 1 y el producto aparece en el carrito con el mismo nombre y precio |

Cada test abre su propio navegador, así que son independientes entre sí.

## Tecnologías

- Python 3.10+
- Selenium WebDriver 4
- Pytest + pytest-html
- Git / GitHub

## Estructura

```
├── datos/
│   └── usuarios.json        # credenciales de prueba
├── reports/                 # reporte HTML, log y capturas de fallos
├── tests/
│   ├── conftest.py          # fixtures (navegador, login) y captura en fallos
│   └── test_saucedemo.py    # casos de prueba
├── utils/
│   ├── helpers.py           # acciones reutilizables (login, carrito, etc.)
│   └── locators.py          # selectores del sitio
├── pytest.ini
└── requirements.txt
```

## Instalación

Requiere Python 3.10 o superior y Google Chrome instalado. El driver de Chrome lo resuelve Selenium solo.

```bash
git clone https://github.com/<tu-usuario>/pre-entrega-automation-testing-haroldo-nogueira.git
cd pre-entrega-automation-testing-haroldo-nogueira

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

## Ejecución

```bash
pytest -v --html=reports/reporte.html --self-contained-html
```

Para correr sin abrir la ventana del navegador:

```bash
HEADLESS=1 pytest -v --html=reports/reporte.html --self-contained-html
```

En Windows (PowerShell): `$env:HEADLESS=1; pytest -v --html=reports/reporte.html --self-contained-html`

## Evidencias

- `reports/reporte.html`: reporte de la última ejecución
- `reports/ejecucion.log`: log con los pasos (login, producto agregado, primer producto del catálogo)
- `reports/screenshots/`: capturas automáticas cuando un test falla
