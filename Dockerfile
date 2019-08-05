
FROM python:3.6
RUN pip install flask gunicorn pymongo Flask-Cors openpyxl pandas

RUN echo hi
ADD flask_app /app
WORKDIR /app
EXPOSE 8080
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app"]
