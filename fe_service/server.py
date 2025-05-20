from flask import Flask, send_from_directory, request, jsonify
import requests

app = Flask(__name__, static_folder="static")

APPOINTMENT_API = "http://localhost:8001/api"
USER_API = "http://localhost:8004/api"

@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/api/login", methods=["POST"])
def api_login():
    resp = requests.post(f"{USER_API}/users/login/", json=request.json)
    return (resp.text, resp.status_code, resp.headers.items())

@app.route("/api/doctor-schedules", methods=["GET"])
def api_doctor_schedules():
    token = request.headers.get("Authorization")
    resp = requests.get(f"{APPOINTMENT_API}/doctor-schedules/", headers={"Authorization": token} if token else {})
    return (resp.text, resp.status_code, resp.headers.items())

@app.route("/api/appointments", methods=["GET", "POST"])
def api_appointments():
    token = request.headers.get("Authorization")
    if request.method == "GET":
        resp = requests.get(f"{APPOINTMENT_API}/appointments/", headers={"Authorization": token} if token else {})
        return (resp.text, resp.status_code, resp.headers.items())
    else:
        resp = requests.post(f"{APPOINTMENT_API}/appointments/", json=request.json, headers={"Authorization": token, "Content-Type": "application/json"} if token else {})
        return (resp.text, resp.status_code, resp.headers.items())

if __name__ == "__main__":
    app.run(port=3000, debug=True)
