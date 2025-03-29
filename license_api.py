from flask import Flask, request, jsonify
from supabase import create_client, Client
from datetime import datetime
import os

app = Flask(__name__)

# Replace with your Supabase project URL and API key
SUPABASE_URL = "https://dwnwexgjjnjxqhdwnwui.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImR3bndleGdqam5qeHFoZHdud3VpIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDMyNDAzMzUsImV4cCI6MjA1ODgxNjMzNX0.puK_yG1V9CYKpMgHTotiN6jkqBGX0dre6Lg1ZihjAtk"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route('/api/check_license', methods=['POST'])
def check_license():
    data = request.get_json()
    license_key = data.get("license_key")
    if not license_key:
        return jsonify({"valid": False}), 400

    # Query the licenses table in Supabase
    result = supabase.table("licenses").select("*").eq("license_key", license_key).execute()
    if result.data:
        lic = result.data[0]
        # Assume expires_at is stored as an ISO formatted string in Supabase
        expires_at_str = lic.get("expires_at")
        try:
            exp_datetime = datetime.fromisoformat(expires_at_str)
        except Exception as e:
            print("Date parsing error:", e)
            return jsonify({"valid": False})
        if datetime.utcnow() < exp_datetime:
            # (Optional) Additional logic to enforce device limits can be added here
            return jsonify({"valid": True})
    return jsonify({"valid": False})

if __name__ == '__main__':
    app.run(debug=True)
