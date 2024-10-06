# None APP (In Progress)

![Python version](https://img.shields.io/badge/Python-3.12-blue?style=flat-square)
[![Continuous integration](https://img.shields.io/github/actions/workflow/status/xgabrielmorales/None/access_guard-ci.yml?style=flat-square&branch=main)](https://github.com/xgabrielmorales/None/actions?query=branch:main)
[![Coverage Status](https://img.shields.io/coverallsCoverage/github/xgabrielmorales/None?branch=main&style=flat-square)](https://coveralls.io/github/xgabrielmorales/None)

None App is an e-commerce platform that demonstrates a simplified microservices architecture. The project is built on a monorepo, with each microservice contained within the [apps](./apps) folder.

![none-app-diagram](https://github.com/user-attachments/assets/e576df81-794a-4959-a7ad-d0a6fa2ebe67)

## Microservices

All of them are written in Python using the [FastAPI](https://fastapi.tiangolo.com/) and [Django](https://www.djangoproject.com/) frameworks. Dependencies are managed using [UV](https://github.com/astral-sh/uv). The project is containerized using [Docker](https://www.docker.com/).

- TODO: [Gate Keeper](./apps/gate_keeper) (API Gateway): Responsible for routing requests to the appropriate microservice.
- [Access Guard](./apps/access_guard) (Authentication Service): Responsible for user authentication and authorization.
- TODO: [Persona Keeper](./apps/persona_keeper) (User Management Service): Responsible for user management.
- [Shop](./apps/shop) (Product Service): Responsible for product and order management.

## TODOS

- [ ] Extract the user manager from the Auth Guard microservice and create a new microservice for it (Persona Keeper).
- [ ] Create the api gateway microservice (Gate Keeper).
- [ ] Add support for inter-dependencies between projects using UV.
- [ ] Test coverage for all microservices individually.
- [ ] Kubernetes (because why not?).
- [ ] Add test, test and more tests.
- [ ] Write a frontend (hmm maybe).
