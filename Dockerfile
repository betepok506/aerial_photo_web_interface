FROM mirror.gcr.io/python:3.10-slim

WORKDIR /web
COPY requirements.txt /web/requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

COPY app /web/app

# CMD python3 -u app/main.py
CMD ["gunicorn", "-b", "0.0.0.0:3000", "app.main:app"]