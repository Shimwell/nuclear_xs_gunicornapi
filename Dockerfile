
FROM python:3.6
RUN pip install flask gunicorn pymongo Flask-Cors openpyxl pandas
RUN apt-get update
RUN apt-get install python-gevent python-gevent-websocket -y

RUN echo hi
ADD flask_app /app
WORKDIR /app
EXPOSE 8080
CMD ["gunicorn", "--timeout", "30", "-b", "0.0.0.0:8000", "app"]