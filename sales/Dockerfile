FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*

COPY ./shared /app/shared

COPY ./sales /app/sales

ENV PIP_DEFAULT_TIMEOUT=100

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5004
ENV FLASK_APP=app.py

CMD ["flask", "run", "--host=0.0.0.0", "--port=5004"]
