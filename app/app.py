from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/hoteles")
def hoteles():
    return render_template("hoteles.html")


@app.route("/reservas")
def reservas():
    return render_template("reservas.html")
