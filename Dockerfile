FROM python:3.8.5

WORKDIR /code
COPY requirements.txt /code
RUN pip install -r requirements.txt
COPY . /code
CMD gunicorn config.wsgi:application --bind 0.0.0.0:8005