FROM python:3.10.6-slim

COPY . .

RUN ["pip", "install", "--no-cache-dir", "--upgrade", "-r", "requirements.txt"]

ENTRYPOINT ["python", "bot.py"]
