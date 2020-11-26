FROM python:3.8.0-alpine
RUN apk add postgresql-dev gcc musl-dev
WORKDIR /usr/src/pollarize
# cache requirements.txt
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .