FROM python:3.10-slim

ENV PATH="/usr/local/bin:${PATH}"

WORKDIR /web
COPY requirements.txt /web/requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

COPY app /web/app

ARG WEB_PORT=5000
ENV WEB_PORT=${WEB_PORT}
EXPOSE $WEB_PORT

RUN echo "${WEB_PORT}"
# CMD python3 -u app/main.py
CMD ["gunicorn", "-b", "0.0.0.0:8000", "app.main:app"]