# Shop
Service to manage products and orders.

## Getting Started

1. Inside the project folder, create a `.env` file and add the following environment variables. You could use the `.env.example` file as a template.
2. Build the Docker image:
   ```bash
   $ docker compose -f docker-compose.dev.yml build
   ```
3. Start the application. Internally, it will start all the necessary services and automatically apply the required migrations to the database.
   ```bash
   $ docker compose -f docker-compose.dev.yml up -d
   ```
4. To run the tests, use the following command:
   ```bash
   $ docker compose -f docker-compose.dev.yml run --rm app pytest
    ```
