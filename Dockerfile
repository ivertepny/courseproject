FROM python:3.12-slim-bookworm

ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-libs \
    musl-dev \
    gcc \
    postgresql-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/* \

COPY ./requirements.txt .

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

COPY . .
