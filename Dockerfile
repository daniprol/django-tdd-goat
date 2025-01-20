FROM python:3.13-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /src

COPY pyproject.toml /src/pyproject.toml
COPY uv.lock /src/uv.lock

# RUN pip install "django<6" gunicorn whitenoise
# RUN pip install -r requirements.txt

# RUN --mount=type=cache,target=/root/.cache/uv \
#     --mount=type=bind,source=uv.lock,target=uv.lock \
#     --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
#     uv sync --frozen --no-install-project

RUN --mount=type=cache,target=/root/.cache/uv uv sync --frozen --no-install-project

# Use absolute paths
COPY src /src

# Sync the project
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen


ENV PATH="/src/.venv/bin:$PATH"
# or use: RUN uv run gunicorn ...

# NOTE: --noinput flag avoids having to confirm anything
RUN ["python", "manage.py", "migrate", "--noinput"]

# TODO: check if we need to add `--ignore "admin"
RUN ["python", "manage.py", "collectstatic"]

ENV DJANGO_DEBUG_FALSE=1
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8888"]
CMD ["gunicorn", "superlists.wsgi:application", "--bind", ":8888", "--access-logfile", "-"]