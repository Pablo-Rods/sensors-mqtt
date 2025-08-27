FROM python:3.12.7

WORKDIR  /app
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

ENTRYPOINT [ "python", "main.py" ]