from flask import Flask, render_template, redirect
from dat import dater

app=Flask(__name__)

@app.route("/")
def defaul():
    return "<!DOCTYPE html><html><body><h1>API is live</h1></body></html>"

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
    d=dater()
    app.run()