FROM python:3.8.9
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD gunicorn app:app

# AWS上にデプロイするときは以下の手順
#  docker build -t netflix --platform amd64 .


