FROM --platform=linux/x86_64 python:3.12-slim

ENV \
  PYTHONUNBUFFERED=1 \
  PYTHONDONTWRITEBYTECODE=1 \
  UV_PROJECT_ENVIRONMENT=/venv

ARG APP_NAME="access_guard"
RUN groupadd --system "${APP_NAME}" \
  && adduser \
  --no-create-home \
  --disabled-password \
  --shell "/sbin/nologin" \
  --ingroup "${APP_NAME}" \
  "${APP_NAME}"

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

RUN \
  --mount=type=cache,target=/root/.cache/uv \
  --mount=type=bind,source=./pyproject.toml,target=./pyproject.toml \
  --mount=type=bind,source=./uv.lock,target=./uv.lock \
  uv sync --locked --dev --no-install-project

WORKDIR /app

ENV PATH "/venv/bin:$PATH"

COPY --chmod=0755 ./compose/dev/start /start

USER ${APP_NAME}
