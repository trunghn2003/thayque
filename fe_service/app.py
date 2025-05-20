import os
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__, template_folder="templates")
CORS(app)

APPOINTMENT_API = os.environ.get("APPOINTMENT_API", "http://localhost:8001/api")
USER_API = os.environ.get("USER_API", "http://localhost:8004/api")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/login", methods=["POST"])
def login():
    data = request.json
    resp = requests.post(f"{USER_API}/users/login/", json=data)
    return (resp.text, resp.status_code, resp.headers.items())

@app.route("/api/doctor-schedules", methods=["GET"])
def get_schedules():
    token = request.headers.get("Authorization")
    resp = requests.get(f"{APPOINTMENT_API}/doctor-schedules/", headers={"Authorization": token} if token else {})
    return (resp.text, resp.status_code, resp.headers.items())

@app.route("/api/appointments", methods=["GET", "POST"])
def appointments():
    token = request.headers.get("Authorization")
    if request.method == "GET":
        resp = requests.get(f"{APPOINTMENT_API}/appointments/", headers={"Authorization": token} if token else {})
        return (resp.text, resp.status_code, resp.headers.items())
    else:
        resp = requests.post(f"{APPOINTMENT_API}/appointments/", json=request.json, headers={"Authorization": token, "Content-Type": "application/json"} if token else {})
        return (resp.text, resp.status_code, resp.headers.items())

if __name__ == "__main__":
    app.run(port=3000, debug=True)
