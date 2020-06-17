FROM python:3.7-stretch

MAINTAINER Pyladies

WORKDIR /myapp

COPY app/ /myapp/app
COPY requirements.txt /myapp

RUN pip install -r requirements.txt

CMD ["python", "app/app.py"]