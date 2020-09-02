from flask import Flask, render_template, redirect
from flask_cors import CORS
from dat import dater

d=dater()

app=Flask(__name__)
CORS(app)

@app.route("/")
def defaul():
    return render_template("index.html")

@app.route("/confirmed_world", methods=['GET'])
def confirmed_world():
    return render_template("confirmed.html")

@app.route("/deaths_world", methods=['GET'])
def deaths_world():
    return render_template("deaths.html")

@app.route("/recovered_world", methods=['GET'])
def recovered_world():
    return render_template("recovered.html")

@app.route("/confirm", methods=['GET'])
def confirm():
    return d.get_total_confirm()

@app.route("/deaths", methods=['GET'])
def deaths():
    return d.get_total_deaths()

@app.route("/recovered", methods=['GET'])
def recover():
    return d.get_total_recov()

if __name__=="__main__":
    app.run()