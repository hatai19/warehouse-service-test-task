FROM python:3.12

WORKDIR /app

COPY requirements.txt ./src/requirements.txt

RUN pip install -r ./src/requirements.txt && pip uninstall -y multipart

COPY . .

CMD ["python", "src/main.py"]