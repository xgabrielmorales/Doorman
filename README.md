# Inicializa el proyecto

1. Dentro de la carpeta del proyecto, crea un archivo .env y adicional las variables de entorno:
    ```bash
    # Base
    # ==============================================================================
    SECRET_KEY=3RWM3zT68QEaOacQiYmSVzNyOHnJMpqVQi8mS2zN

    # Postgres DB
    # ==============================================================================
    POSTGRES_DB=example-db
    POSTGRES_PASSWORD=e8617cc1dccfbeefe3777f6816bd6cce
    POSTGRES_HOST=example-postgres-db
    POSTGRES_USER=example-db
    ```

2. Haz build de la imagen de docker con el siguiente comando:
   ```bash
   $ docker compose -f docker-compose.dev.yml build
   ```

3. Levanta el servicio de la base de datos y aplica las migraciones:
   ```bash
   $ docker compose -f docker-compose.dev.yml up -d app-postgres-db
   ```
   ```bash
   $ docker compose -f docker-compose.dev.yml run --rm app alembic upgrade head
   ```

4. Levanta todos los servicios restantes:
   ```bash
   $ docker compose -f docker-compose.dev.yml up -d
   ```
5. Como adicional para ejecutar los tests utiliza el comando:
   ```bash
   $ docker compose -f docker-compose.test.yml run --rm app pytest
   ```
