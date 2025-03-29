# api/app.py
import os
from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from datetime import datetime, timedelta

app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = os.environ.get("SECRET_KEY", "default_secret_key")

# Dummy license data for demonstration
licenses = [
    {
        "id": 1,
        "license_key": "VALID_KEY",
        "expires_at": datetime.utcnow() + timedelta(days=30),
        "device_limit": 1,
        "active_devices": 0
    }
]

# License API endpoint
@app.route("/api/check_license", methods=["POST"])
def check_license():
    data = request.get_json()
    license_key = data.get("license_key")
    for lic in licenses:
        if lic["license_key"] == license_key and datetime.utcnow() < lic["expires_at"]:
            return jsonify({"valid": True})
    return jsonify({"valid": False})

# Admin dashboard: List licenses
@app.route("/")
def dashboard():
    return render_template("dashboard.html", licenses=licenses)

# Route to create a new license
@app.route("/create_license", methods=["GET", "POST"])
def create_license():
    if request.method == "POST":
        license_key = request.form["license_key"]
        duration_days = int(request.form["duration"])
        device_limit = int(request.form["device_limit"])
        expires_at = datetime.utcnow() + timedelta(days=duration_days)
        new_license = {
            "id": len(licenses) + 1,
            "license_key": license_key,
            "expires_at": expires_at,
            "device_limit": device_limit,
            "active_devices": 0
        }
        licenses.append(new_license)
        flash("License created successfully!", "success")
        return redirect(url_for("dashboard"))
    return render_template("create_license.html")

if __name__ == "__main__":
    app.run(debug=True)
