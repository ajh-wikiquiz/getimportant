FROM docker.io/tiangolo/uvicorn-gunicorn-fastapi:python3.8

COPY requirements.txt /app/app/requirements.txt
RUN pip install -r /app/app/requirements.txt

COPY ./app /app/app
