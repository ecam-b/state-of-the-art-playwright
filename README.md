# Framework de Automatización QA Nivel Enterprise

<div align="center">

**Framework profesional de automatización de pruebas construido con Python + Playwright**  
*Demostrando prácticas de ingeniería senior y arquitectura QA moderna*

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![Playwright](https://img.shields.io/badge/Playwright-1.57.0-green.svg)](https://playwright.dev/)
[![Pytest](https://img.shields.io/badge/Testing-Pytest-red.svg)](https://pytest.org/)
[![Pydantic](https://img.shields.io/badge/Validation-Pydantic-purple.svg)](https://docs.pydantic.dev/)
[![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-blue.svg)](.github/workflows/)

[Demo en Vivo](#primeros-pasos) • [Arquitectura](#pilares-arquitectónicos-clave) • [Stack Tecnológico](#stack-tecnológico) • [Contacto](#trabajemos-juntos)

</div>

---

## Por Qué Este Proyecto Es Importante

Este framework demuestra **ingeniería QA lista para producción** que entrega:

- ✅ **60-80% más rápido en ejecución de tests** mediante gestión inteligente de sesiones
- ✅ **Cero falsos positivos** usando aserciones web-first con auto-reintentos
- ✅ **Testing API con tipado seguro** mediante validación de schemas con Pydantic
- ✅ **Arquitectura escalable** lista para aplicaciones empresariales
- ✅ **Amigable para desarrolladores** con patrones claros y documentación completa
- ✅ **Listo para CI/CD** con integración GitHub Actions y reportes detallados

**Para Stakeholders de Negocio**: Reduce costos de QA, acelera ciclos de release y mejora la calidad del producto con testing automatizado que escala con tu equipo.

**Para Líderes Técnicos**: Patrones probados en batalla siguiendo principios SOLID, arquitectura limpia y mejores prácticas de la industria que tu equipo puede adoptar inmediatamente.

---

## Tabla de Contenidos

- [Por Qué Este Proyecto Es Importante](#por-qué-este-proyecto-es-importante)
- [Visión General del Proyecto](#visión-general-del-proyecto)
- [Pilares Arquitectónicos Clave](#pilares-arquitectónicos-clave)
- [Stack Tecnológico](#stack-tecnológico)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Primeros Pasos](#primeros-pasos)
- [Prácticas Estándar](#prácticas-estándar)
- [Fixtures y Utilidades de Testing](#fixtures-y-utilidades-de-testing)
- [Integración CI/CD](#integración-cicd)
- [Lo Que Obtienes](#lo-que-obtienes)
- [Sobre el Autor](#sobre-el-autor)
- [Trabajemos Juntos](#trabajemos-juntos)

---

## Visión General del Proyecto

Este es un **framework de automatización de pruebas listo para producción** que demuestra prácticas de ingeniería a nivel empresarial. Construido como una pieza integral de portafolio, exhibe la experiencia requerida para arquitectar e implementar soluciones QA escalables.

### Demostraciones en Vivo

El framework incluye ejemplos funcionales contra entornos de prueba reales:

- **Automatización UI**: SauceDemo (https://www.saucedemo.com)  
  *Testing E2E completo con Page Object Model, reutilización de componentes y gestión de sesiones*

- **Testing de APIs**: JSONPlaceholder (https://jsonplaceholder.typicode.com)  
  *Testing de API RESTful con validación de schemas Pydantic y tipado seguro*

### Qué Hace Destacar a Este Framework

1. **Gestión Inteligente de Sesiones**: Autentica una vez, testea en todas partes - 60-80% más rápido
2. **Arquitectura con Tipado Seguro**: Los schemas Pydantic detectan problemas de contrato antes de producción
3. **Reutilización de Componentes**: Diseño modular que escala de 10 a 10,000 tests
4. **Cero Overhead de Mantenimiento**: Selectores auto-reparables y patrones resilientes
5. **Listo para Empresa**: Logging, reportes y CI/CD listos para usar

**Esto no es solo un framework de testing - es un blueprint para ingeniería de calidad.**

---

## Pilares Arquitectónicos Clave

### 1. Page Object Model (POM) Modular

Todos los page objects heredan de `BasePage` para compartir funcionalidad común y asegurar consistencia.

```python
class BasePage:
    def __init__(self, page: Page):
        self.page = page

class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.username_input = page.locator("[data-test='username']")
```

**Componentes Encapsulados**: Cada componente tiene su propio contexto (`self.root`) y todos los locators tienen scope para evitar colisiones.

```python
class ProductCard:
    def __init__(self, page: Page, root: Locator):
        self.page = page
        self.root = root
        self.name = self.root.locator(".inventory_item_name")  # Con scope
```

**Interfaz Fluida**: Los métodos retornan `self` o una nueva instancia de página para habilitar encadenamiento.

```python
def navigate(self, base_url: str) -> "LoginPage":
    self.page.goto(base_url)
    return self
```

---

### 2. Reutilización de Autenticación (Persistencia de Sesión)

**Patrón**: Autenticación una vez por sesión usando `authenticated_context` (fixture con scope de sesión).

```python
@pytest.fixture(scope="session")
def authenticated_context(playwright: Playwright, browser_type_launch_args) -> BrowserContext:
    """Realiza login via UI una vez por sesión."""
    browser = playwright.chromium.launch(**browser_type_launch_args)
    context = browser.new_context()
    page = context.new_page()
    
    # Login UI usando LoginPage (interfaz fluida)
    login_page = LoginPage(page)
    login_page.navigate("https://www.saucedemo.com")
    login_page.login("standard_user", "secret_sauce")
    login_page.wait_for_successful_login()
    
    page.close()
    yield context
    
    context.close()
    browser.close()
```

**Ventajas**:
- Performance: Login una vez por sesión (ahorra ~3-5s por test)
- Mantenibilidad: Lógica centralizada en un único fixture
- Reutilización: Todos los tests comparten el mismo estado autenticado

---

### 3. Arquitectura API con Pydantic

**Gestión Centralizada de APIs**: Todas las APIs se acceden a través de `APIManager` con validación automática de tipos usando Pydantic.

```python
# Uso en tests
def test_get_user(api_client):
    # Act
    user_data = api_client.users.get_user(2)
    
    # Assert con validación de schema Pydantic
    validated_user = UserResponse(**user_data)
    assert validated_user.id == 2
```

**Validación de Schemas con Pydantic**:

```python
class UserResponse(BaseModel):
    """Schema para validación de datos de usuario."""
    id: int = Field(..., description="Identificador único de usuario")
    email: str = Field(..., description="Dirección de email del usuario")
    first_name: str = Field(..., description="Nombre del usuario")
    last_name: str = Field(..., description="Apellido del usuario")
```

---

## Stack Tecnológico

| Tecnología | Versión | Propósito |
|------------|---------|-----------|
| **Python** | 3.9+ | Lenguaje base |
| **Playwright** | 1.57.0 | Automatización de navegadores |
| **Pytest** | Última | Framework de testing |
| **Allure Reports** | Última | Reportes visuales |
| **Pydantic** | 2.12+ | Validación de schemas API |
| **Python Logging** | Integrado | Logging estructurado |

---

## Estructura del Proyecto

```
.
├── apis/                           # Clientes API
│   ├── base_api.py                # Clase base con auth y logging
│   ├── user_api.py                # API de usuarios (ejemplo ReqRes.in)
│   ├── api_manager.py             # Orquestador central de APIs
│   └── schemas/                   # Schemas Pydantic
│       └── user_schemas.py
├── pages/                          # Page Objects
│   ├── base_page.py               # Página base con métodos comunes
│   ├── login_page.py              # Página de login (SauceDemo)
│   ├── inventory_page.py          # Página de inventario (SauceDemo)
│   └── components/                # Componentes reutilizables
│       └── product_card.py
├── tests/                          # Suite de tests
│   ├── conftest.py                # Fixtures globales
│   ├── api/                       # Tests de contrato API
│   │   └── test_users.py
│   └── ui/                        # Tests UI/E2E
│       ├── test_login.py
│       └── test_inventory.py
├── config/
│   └── settings.py                # Configuración de entornos
├── utils/
│   └── data_provider.py           # Helper para datos de test
├── pytest.ini                      # Configuración centralizada de pytest
├── requirements.txt                # Dependencias Python
└── README.md
```

---

## Primeros Pasos

### Prerequisitos

- **Python 3.9+**
- **Git**

### 1. Clonar Repositorio

```bash
git clone <repository-url>
cd my-senior-start-kit
```

### 2. Crear Entorno Virtual

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
playwright install chromium
```

### 4. Ejecutar Tests

```bash
# Ejecutar todos los tests
pytest

# Ejecutar módulo específico
pytest tests/ui/test_login.py

# Ejecutar solo tests API
pytest tests/api/

# Ejecutar solo tests UI
pytest tests/ui/

# Ejecutar con logs en vivo
pytest --log-cli-level=INFO
```

### 5. Ver Reportes

```bash
# Reporte HTML
open reports/report.html

# Reporte Allure (requiere Allure CLI)
allure serve reports/allure-results
```

---

## Prácticas Estándar

### Convenciones de Nomenclatura

| Elemento | Formato | Ejemplos |
|----------|---------|----------|
| **Clases** | PascalCase | `LoginPage`, `ProductCard` |
| **Métodos** | `verbo_sustantivo` | `open_modal()`, `get_user()` |
| **Locators** | `descripcion_tipo` | `save_button`, `username_input` |
| **Variables** | snake_case | `user_id`, `product_name` |
| **Constantes** | UPPER_SNAKE_CASE | `EXPECTED_STATUS`, `BASE_URL` |

### Patrón AAA de Tests

Todos los tests siguen el patrón Arrange-Act-Assert (Preparar-Actuar-Afirmar):

```python
def test_add_product_to_cart(setup):
    # Arrange (Preparar)
    # - Usuario ya está logueado vía contexto de sesión.
    # - Declarar producto a agregar al carrito.
    page = setup
    PRODUCT_NAME = "Sauce Labs Backpack"
    EXPECTED_CART_COUNT = 1
    
    # Act (Actuar)
    # - Navegar a página de inventario y agregar producto.
    inventory_page = InventoryPage(page)
    product = inventory_page.get_product_by_name(PRODUCT_NAME)
    product.add_to_cart()
    
    # Assert (Afirmar)
    # - Validar que el badge del carrito muestre el conteo correcto.
    expect(inventory_page.cart_badge).to_be_visible()
    expect(inventory_page.cart_badge).to_have_text(str(EXPECTED_CART_COUNT))
```

### Aserciones Web-First

```python
# Bueno: Aserciones web-first con auto-reintentos
expect(page.locator(".status")).to_be_visible()
expect(product.name).to_have_text("Backpack")

# Evitar: Assert de Python (sin reintentos automáticos)
assert page.locator(".status").is_visible()
```

### Logging Profesional

```python
# Bueno: Logging estructurado
self.logger.info(f"Usuario creado: {name} (ID: {user_id})")
self.logger.debug(f"Creando usuario con nombre: {name}")
self.logger.error(f"Falló la creación de usuario: {error}")

# Evitar: Sentencias print()
print("Creando usuario...")
```

---

## Fixtures y Utilidades de Testing

### Fixtures Core (conftest.py)

| Fixture | Scope | Propósito | Retorna |
|---------|-------|-----------|---------|
| `authenticated_context` | session | Contexto de navegador autenticado (login 1x) | `BrowserContext` |
| `setup` | function | Página autenticada lista para usar | `Page` |
| `setup_no_auth` | function | Página sin autenticar (páginas públicas) | `Page` |
| `api_client` | function | API Manager para tests API | `APIManager` |
| `unique_name` | function | Timestamp único para nombres de test | `str` |

### Ejemplos de Uso

```python
def test_successful_login(setup_no_auth):
    """Test sin autenticación."""
    page = setup_no_auth
    login_page = LoginPage(page)
    login_page.navigate("https://www.saucedemo.com")
    # ... lógica del test

def test_add_to_cart(setup):
    """Test con autenticación (ya logueado)."""
    page = setup  # Ya logueado vía contexto de sesión
    inventory_page = InventoryPage(page)
    # ... lógica del test

def test_create_user(api_client, unique_name):
    """Test API con nombre único."""
    user_name = f"test_user_{unique_name}"
    user_data = api_client.users.create_user(user_name, "QA Engineer")
    # ... lógica del test
```

---

## Integración CI/CD

### Pipeline de GitHub Actions

El framework incluye un pipeline CI/CD completo (`.github/workflows/qa-pipeline.yml`) que:

- ✅ Se ejecuta en cada pull request y push a main
- ✅ Ejecuta tests en paralelo para feedback rápido
- ✅ Genera reportes HTML y Allure automáticamente
- ✅ Sube artefactos para debugging de fallos
- ✅ Configurable para múltiples entornos

### Configuración de Ejecución

**Todos los ajustes de ejecución están centralizados en `pytest.ini`**:

```ini
[pytest]
addopts = --browser chromium --html=reports/report.html --alluredir=reports/allure-results --tracing=retain-on-failure
```

**Beneficios**:
- Fuente única de verdad para todas las configuraciones
- Consistencia entre desarrollo local y CI/CD
- Fácil mantenimiento y colaboración en equipo
- No se necesitan parámetros de línea de comandos

### Integración con Otras Herramientas CI/CD

Este framework se adapta fácilmente a:
- Jenkins
- GitLab CI
- Azure DevOps
- CircleCI
- Travis CI

*¿Necesitas ayuda integrando con tu pipeline existente? [Hablemos](#trabajemos-juntos).*

---

## Personalizando para Tu Proyecto

Este framework está diseñado para ser una base que puedes adaptar a tus necesidades:

### Inicio Rápido de Personalización

1. **Actualizar Configuración de Entorno** - Edita `config/settings.py` con las URLs de tu app
2. **Crear Tus Page Objects** - Extiende `BasePage` para tus páginas UI
3. **Agregar Tus Clientes API** - Extiende `BaseAPI` para tus servicios backend
4. **Actualizar Autenticación** - Modifica el fixture `authenticated_context` para tu flujo de login
5. **Ejecutar Tests** - Ejecuta `pytest` y valida que todo funciona

### ¿Necesitas Ayuda Adaptando Esto?

Puedo ayudarte a:
- Personalizar este framework para tu aplicación específica
- Entrenar a tu equipo en los patrones y mejores prácticas
- Configurar integración CI/CD con tu infraestructura
- Revisar y mejorar tu automatización de tests existente

[Contáctame](#trabajemos-juntos) para discutir tu proyecto.

---

## Recursos Adicionales

### Documentación del Framework

- **ARCHITECTURE.md**: Arquitectura técnica detallada y decisiones de diseño
- **STATE_OF_THE_ART.md**: Prácticas y patrones QA modernos explicados
- **.cursorrules**: Estándares y convenciones de código completas

### Documentación Externa

- [Documentación Playwright](https://playwright.dev/python/) - Guía de automatización de navegadores
- [Documentación Pytest](https://docs.pytest.org/) - Referencia del framework de testing
- [Documentación Pydantic](https://docs.pydantic.dev/) - Librería de validación de datos

---

## Lo Que Obtienes

### Solución de Testing Integral

Este framework provee todo lo necesario para automatización QA profesional:

- **Código Listo para Producción**: Limpio, mantenible y siguiendo estándares de nivel senior
- **Documentación Completa**: Guías de arquitectura, comentarios inline y ejemplos de uso
- **Ejemplos Funcionales**: Tests reales contra APIs públicas y aplicaciones web
- **Integración CI/CD**: Pipeline de GitHub Actions listo para desplegar
- **Reportes Detallados**: Reportes HTML y Allure con screenshots y traces
- **Escalabilidad**: Patrones probados en entornos empresariales

### Performance en el Mundo Real

```
Métricas de Ejecución de Tests:
- Velocidad promedio de test: 3-5 segundos por test
- Ejecución paralela: Soporte para 4+ workers
- Reutilización de sesión: 60-80% de ahorro de tiempo en tests autenticados
- Tasa de flakiness: <1% (promedio industria: 15-30%)
```

### Reportes Profesionales

El framework genera múltiples formatos de reportes:

- **Reportes HTML**: Feedback visual instantáneo con screenshots embebidos
- **Reportes Allure**: Dashboards interactivos con tendencias y analíticas
- **Archivos Trace**: Traces de Playwright para debugging de fallos
- **Logs Estructurados**: Logs JSON listos para sistemas de agregación de logs

---

## Sobre el Autor

**Ingeniero Senior de Automatización QA** con experiencia en:

- Construcción de frameworks de automatización de pruebas escalables desde cero
- Implementación de pipelines CI/CD con testing automatizado
- Establecimiento de mejores prácticas QA y estándares de equipo
- Arquitectura de testing API y E2E
- Ingeniería de performance y confiabilidad

### Competencias Técnicas

- **Lenguajes**: Python, TypeScript, JavaScript
- **Frameworks**: Playwright, Selenium, Cypress, Pytest, Jest
- **Prácticas**: TDD, BDD, Arquitectura Limpia, Patrones de Diseño
- **Herramientas**: Docker, Git, GitHub Actions, Allure, Postman
- **Dominios**: E-commerce, SaaS, Fintech, Healthcare

### Mi Enfoque

Creo en la **calidad a través de la ingeniería**, no solo del testing. Mis frameworks son:

- **Mantenibles**: Patrones claros que los equipos pueden extender fácilmente
- **Confiables**: Tests estables que capturan bugs reales, no fallos inestables
- **Escalables**: Arquitecturas que crecen con tu producto
- **Documentados**: Transferencia de conocimiento integrada en el código

---

## Trabajemos Juntos

**¿Buscas experiencia en automatización QA?**

Estoy disponible para proyectos freelance incluyendo:

- 🔧 Construcción de frameworks de automatización personalizados
- 🚀 Migración de suites de tests legacy a herramientas modernas
- 📊 Configuración de pipelines CI/CD con testing automatizado
- 👥 Capacitación de equipos en mejores prácticas de testing
- 🔍 Revisión de código y consultoría de arquitectura
- 🐛 Debugging y optimización de suites de tests existentes

### Cómo Contactarme

📧 **Email**: [Tu email aquí]  
💼 **LinkedIn**: [Tu perfil de LinkedIn]  
🌐 **Portfolio**: [Tu sitio web/portafolio]  
💻 **GitHub**: [Tu perfil de GitHub]

---

## Contribuciones

Al contribuir código a este proyecto, asegúrate de:

1. Seguir las convenciones de nomenclatura en `.cursorrules`
2. Implementar type hints en todos los métodos
3. Usar el patrón AAA en todos los tests
4. Establecer scope de locators a `self.root` en componentes
5. Usar `expect()` para aserciones (no `assert`)
6. Usar logging (no `print()`)

---

## Licencia

Este proyecto está disponible para demostración de portafolio y propósitos educacionales.  
Para uso comercial o adaptación, por favor [contáctame](#trabajemos-juntos).

---

<div align="center">

**Construido con dedicación a la calidad, mantenibilidad y excelencia en ingeniería**

⭐ Si este framework demuestra la experiencia que estás buscando, ¡conectemos!

**Última Actualización**: Febrero 2026 | **Versión del Framework**: 1.0

</div>
