# 1. Usamos una imagen oficial de Python como base
FROM python:3.12-slim

# 2. Definimos dónde vivirá nuestro código dentro del contenedor
WORKDIR /app

# Optimizamos: instalamos dependencias del sistema primero
RUN apt-get update && apt-get install -y \
    libnss3 \
    libnspr4 \
    libgbm1 \
    libasound2 \
    && rm -rf /var/lib/apt/lists/*

# 3. Copiamos tu archivo de dependencias
COPY requirements.txt .

# 4. Instalamos las librerías (pytest, playwright, etc.)
RUN pip install --no-cache-dir -r requirements.txt

# 5. PASO CLAVE PARA QA: Instalamos los navegadores de Playwright
# El comando 'install-deps' instala las librerías del sistema necesarias
RUN playwright install --with-deps chromium

# 6. Copiamos todo el resto de tu código de pruebas al contenedor
COPY . .

# 7. El comando que se ejecutará por defecto al iniciar el contenedor
CMD ["pytest"]