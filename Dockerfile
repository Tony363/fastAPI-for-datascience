FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7
COPY ./my_API /app

RUN pip install -r requirements.txt