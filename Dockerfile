FROM python:3.7-slim-buster

RUN apt update -y

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

CMD ['streamlit', 'run', 'app.py', "--server.port=8501", "--server.address=0.0.0.0"]