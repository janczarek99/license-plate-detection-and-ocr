FROM python:3.9.7-slim-buster

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

RUN python -m pip install pip==21.3.1

COPY requirements.txt .
RUN pip install -r requirements.txt

WORKDIR /app

COPY ./src ./src/

EXPOSE 80

CMD ["uvicorn", "src:app", "--host", "0.0.0.0", "--port", "80"]
# CMD ["gunicorn", "--bind=0.0.0.0:80", "--workers=4", "--timeout=500", "--threads=1", "src:app"]
