FROM python:3.9-slim as dev

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

FROM dev AS prod

COPY . .