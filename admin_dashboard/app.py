from flask import Flask, render_template, request, redirect, url_for, flash
from supabase import create_client, Client
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = "your_secret_key_here"

# Replace with your Supabase project URL and API key
SUPABASE_URL = "https://dwnwexgjjnjxqhdwnwui.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImR3bndleGdqam5qeHFoZHdud3VpIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDMyNDAzMzUsImV4cCI6MjA1ODgxNjMzNX0.puK_yG1V9CYKpMgHTotiN6jkqBGX0dre6Lg1ZihjAtk"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route('/')
def dashboard():
    result = supabase.table("licenses").select("*").execute()
    licenses = result.data if result.data else []
    return render_template("dashboard.html", licenses=licenses)

@app.route('/create_license', methods=['GET', 'POST'])
def create_license():
    if request.method == 'POST':
        license_key = request.form['license_key']
        duration_days = int(request.form['duration'])
        device_limit = int(request.form['device_limit'])
        expires_at = datetime.utcnow() + timedelta(days=duration_days)
        # Insert new license into Supabase
        result = supabase.table("licenses").insert({
            "license_key": license_key,
            "expires_at": expires_at.isoformat(),
            "device_limit": device_limit,
            "active_devices": 0
        }).execute()
        if result.data:
            flash("License created successfully!", "success")
        else:
            flash("Error creating license.", "danger")
        return redirect(url_for('dashboard'))
    return render_template("create_license.html")

if __name__ == '__main__':
    app.run(debug=True)
