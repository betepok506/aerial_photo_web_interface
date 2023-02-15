from flask import Flask, render_template, flash, request, redirect, url_for
from flask_bootstrap import Bootstrap5

app = Flask(__name__)
Bootstrap5(app)

app.config['SECRET_KEY'] = 'any secret string'
app.config['BOOTSTRAP_BOOTSWATCH_THEME'] = 'pulse'


@app.route("/", methods=["POST", "GET"])
def map():
    return render_template("map.html")


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8000)
