FROM python:3.9-slim-bullseye

WORKDIR /app

COPY ./my_flask_app /app
COPY requirements.txt /app/
COPY ./my_flask_app/model/model_pipeline.pkl /app/model/model_pipeline.pkl



RUN pip install requirements.txt

EXPOSE 5000

CMD ["python", "app.py"]
