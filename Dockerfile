FROM python:latest
LABEL authors="c42759"

WORKDIR /code

COPY ./*.py .
COPY requirements.txt .

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "app.py"]