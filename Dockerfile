FROM python:3.9-slim-bullseye

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY ./my_flask_app /app
COPY ./my_flask_app/model/model_pipeline.pkl /app/model/model_pipeline.pkl

EXPOSE 5001   

CMD ["python", "app.py"]