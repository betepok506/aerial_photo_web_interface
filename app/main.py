import logging
import os

import requests
from flask import Flask, render_template, flash, request, redirect, url_for
from flask_bootstrap import Bootstrap5
from logger import get_file_handler

app = Flask(__name__)
Bootstrap5(app)

app.config['SECRET_KEY'] = 'any secret string'
app.config['BOOTSTRAP_BOOTSWATCH_THEME'] = 'pulse'
SERVER_URL = os.getenv("SERVER_HOST", "127.0.0.1") + ":" + str(os.getenv("SERVER_PORT", 8001))
app.logger.addHandler(get_file_handler())
app.logger.setLevel(logging.INFO)


@app.route("/", methods=["POST", "GET"])
def map():
    class_objects = []
    try:
        response = requests.get(f'http://{SERVER_URL}/classes_query')
        if response.status_code == 200:
            class_objects = response.json()
    except Exception as error_connection:
        app.logger.warning(f'Error {error_connection} occurred when trying to connect '
                           f'to http://{SERVER_URL}/classes_query')

    return render_template("map.html", class_objects=class_objects)


@app.route("/polygon_object_by_lat_lng", methods=["POST", "GET"])
def polygon_object_by_lat_lng():
    polygons = {"polygons": []}
    if request.method == 'POST':
        lat_min = request.form.get('lat_min')
        lng_min = request.form.get('lng_min')
        lat_max = request.form.get('lat_max')
        lng_max = request.form.get('lng_max')
        cls_obj = request.form.getlist('cls_obj[]')
        try:
            response = requests.post(
                f'http://{SERVER_URL}/polygon_object_by_lat_lng/', json={
                    "lat_min": float(lat_min),
                    "lng_min": float(lng_min),
                    "lat_max": float(lat_max),
                    "lng_max": float(lng_max),
                    "cls_obj": cls_obj
                })
            if response.status_code == 200:
                polygons["polygons"] = response.json()
        except Exception as error_connection:
            app.logger.warning(f'Error {error_connection} occurred when trying to connect '
                               f'to http://{SERVER_URL}/polygon_object_by_lat_lng/')

    return polygons


#
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=os.getenv("WEB_PORT", 8000))
