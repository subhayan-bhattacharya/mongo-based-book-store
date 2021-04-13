FROM python:3.8

LABEL maintainer="poulomi.adhikari.88@gmail.com"

RUN apt-get update -y

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt

CMD ["python", "app.py"]



