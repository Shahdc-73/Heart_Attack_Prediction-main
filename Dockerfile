FROM python:3.9-slim

WORKDIR /app

COPY ./my_flask_app /app
COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python", "app.py"]
