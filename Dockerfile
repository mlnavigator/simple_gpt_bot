FROM python:3.10-alpine3.18

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

CMD ["python", "./tg_bot.py"]
