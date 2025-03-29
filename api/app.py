# api/app.py
import os
from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from datetime import datetime, timedelta
from supabase import create_client, Client

app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = os.environ.get("SECRET_KEY", "default_secret_key")

# Supabase configuration (using provided details as defaults)
SUPABASE_URL = os.environ.get("SUPABASE_URL", "https://dwnwexgjjnjxqhdwnwui.supabase.co")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImR3bndleGdqam5qeHFoZHdud3VpIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDMyNDAzMzUsImV4cCI6MjA1ODgxNjMzNX0.puK_yG1V9CYKpMgHTotiN6jkqBGX0dre6Lg1ZihjAtk")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_license_info(license_key):
    response = supabase.table("licenses").select("*").eq("license_key", license_key).execute()
    data = response.data
    if data and len(data) > 0:
        return data[0]
    return None

# License API endpoint for desktop validation
@app.route("/api/check_license", methods=["POST"])
def check_license_api():
    data = request.get_json()
    license_key = data.get("license_key")
    lic = get_license_info(license_key)
    if lic:
        expires_at = lic.get("expires_at")
        # Convert ISO string to datetime if necessary
        if isinstance(expires_at, str):
            expires_at = datetime.fromisoformat(expires_at)
        if datetime.utcnow() < expires_at:
            return jsonify({"valid": True})
    return jsonify({"valid": False})

# Admin dashboard: List licenses
@app.route("/")
def dashboard():
    response = supabase.table("licenses").select("*").execute()
    licenses = response.data or []
    return render_template("dashboard.html", licenses=licenses)

# Route to create a new license
@app.route("/create_license", methods=["GET", "POST"])
def create_license():
    if request.method == "POST":
        license_key = request.form["license_key"]
        duration_days = int(request.form["duration"])
        device_limit = int(request.form["device_limit"])
        expires_at = (datetime.utcnow() + timedelta(days=duration_days)).isoformat()
        data_to_insert = {
            "license_key": license_key,
            "expires_at": expires_at,
            "device_limit": device_limit,
            "active_devices": 0
        }
        response = supabase.table("licenses").insert(data_to_insert).execute()
        if response.status_code in [200, 201]:
            flash("License created successfully!", "success")
        else:
            flash("Error creating license: " + str(response.error), "danger")
        return redirect(url_for("dashboard"))
    return render_template("create_license.html")

# Route to delete a license by license_key
@app.route("/delete_license/<string:license_key>", methods=["POST"])
def delete_license(license_key):
    response = supabase.table("licenses").delete().eq("license_key", license_key).execute()
    if response.status_code == 200:
        flash("License deleted successfully!", "success")
    else:
        flash("Error deleting license: " + str(response.error), "danger")
    return redirect(url_for("dashboard"))

if __name__ == "__main__":
    app.run(debug=True)
