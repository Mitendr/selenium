FROM python:3.9.12-slim-bullseye

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

CMD ["pytest"]
