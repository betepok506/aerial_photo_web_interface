FROM python:3.8-slim

WORKDIR /web
COPY requirements.txt /web/requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

COPY app /web/app

CMD python3 -u app/main.py
