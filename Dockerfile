FROM python:3.6.0-slim
WORKDIR /app
ENV PYTHONUNBUFFERED=1
ADD . /app/
RUN pip install --upgrade pip && pip install -r requirements.txt
