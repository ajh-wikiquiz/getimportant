FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8-slim

COPY ./app requirements.txt /app/app/
RUN pip install -r /app/app/requirements.txt
