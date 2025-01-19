FROM python:3.13-slim

RUN python -m venv /venv

ENV PATH="/venv/bin:$PATH"

RUN pip install "django<6" gunicorn whitenoise
# RUN pip install -r requirements.txt

COPY src /src


WORKDIR /src

# NOTE: --noinput flag avoids having to confirm anything
RUN ["python", "manage.py", "migrate", "--noinput"]

# CMD ["python", "manage.py", "runserver", "0.0.0.0:8888"]
CMD ["gunicorn", "superlists.wsgi:application", "--bind", ":8888", "--access-logfile", "-"]