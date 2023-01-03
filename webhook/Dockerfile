FROM python:3.9.13-slim-bullseye

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY ./app.py /app

COPY ./docker-entrypoint.sh /

EXPOSE 5000

ENTRYPOINT ["sh", "/docker-entrypoint.sh"]
