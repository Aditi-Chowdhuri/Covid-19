from flask import Flask, render_template, redirect, request
from flask_cors import CORS
from dat import dater

d=dater()

app=Flask(__name__)
CORS(app)

@app.route("/", methods=['GET', 'POST'])
def defaul():
    return render_template("index.html", country=d.countries)

@app.route("/confirm", methods=['GET', 'POST'])
def confirm():
    if request.method=="POST":
        c=request.form["country"]
        return d.get_total_confirm(c)
    return "NAN"

@app.route("/deaths", methods=['GET', 'POST'])
def deaths():
    if request.method=="POST":
        c=request.form["country"]
        return d.get_total_deaths(c)
    return "NAN"

@app.route("/recovered", methods=['GET', 'POST'])
def recover():
    if request.method=="POST":
        c=request.form["country"]
        return d.get_total_recov(c)
    return "NAN"

@app.route("/daily_confirmed", methods=['GET', 'POST'])
def daily_confirmed():
    if request.method=="POST":
        c=request.form["country"]
        return d.get_daily_confirmed_world(c)
    return "NAN"

if __name__=="__main__":
    app.run(debug=True)