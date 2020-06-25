FROM python:3.8

RUN mkdir -p /app/
COPY . /app/

RUN pip install -r /app/src/requirements.txt

WORKDIR /app/src

CMD ["python", "run.py"]