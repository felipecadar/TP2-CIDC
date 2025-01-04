FROM python:3.11-slim

WORKDIR /app
RUN apt-get update && apt-get install -y gcc
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "train.py"]