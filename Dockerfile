FROM python:3.8.9
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .
ENV PORT 5000
EXPOSE 5000

CMD ["python", "app.py"]




