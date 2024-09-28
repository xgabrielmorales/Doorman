# Doorman
![Python version](https://img.shields.io/badge/Python-3.12-blue?style=flat-square)
[![Continuous integration](https://img.shields.io/github/actions/workflow/status/xgabrielmorales/None/ci.yml?style=flat-square)](https://github.com/xgabrielmorales/None/actions?query=branch:main)
[![Coverage Status](https://img.shields.io/coverallsCoverage/github/xgabrielmorales/None?branch=main&style=flat-square)](https://coveralls.io/github/xgabrielmorales/None)

## Inicializa el proyecto

1. Dentro de la carpeta del proyecto, crea un archivo `.env` y adicional las variables de entorno:
    <details>
    <summary>Haz clic aquí para usar las de ejemplo</summary>

    ```bash
    # Base
    # ==============================================================================
    SECRET_KEY=3RWM3zT68QEaOacQiYmSVzNyOHnJMpqVQi8mS2zN

    # Postgres DB
    # ==============================================================================
    POSTGRES_HOST=postgres-db
    POSTGRES_DB=example-db-db
    POSTGRES_USER=example-user-db
    POSTGRES_PASSWORD=example-password-db
    ```

    </details>

2. Haz el build de la imagen de Docker.:
   ```bash
   $ docker compose -f docker-compose.dev.yml build
   ```
3. Levanta la aplicación. Internamente, levantará todos los servicios necesarios y automáticamente aplicará las migraciones requeridas a la base de datos.
   ```bash
   $ docker compose -f docker-compose.dev.yml up -d
   ```
4. Para ejecutar los tests usa el siguiente comando:
   ```bash
   $ docker compose -f docker-compose.dev.yml run --rm app pytest
   ```
