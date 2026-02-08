FROM python:3.11-slim

WORKDIR /app
COPY . .

ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

ENV PYTHONUNBUFFERED=1

CMD ["python", "-u", "TaskManager.py"]