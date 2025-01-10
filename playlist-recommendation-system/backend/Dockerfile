# docker file for flask app
FROM python:3.11-slim

WORKDIR /app
RUN mkdir -p /app/logs

COPY requirements.txt requirements.txt
RUN apt-get update && apt-get install -y gcc
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "app.py"]
