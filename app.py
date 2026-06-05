from flask import Flask, jsonify
import requests
import pandas as pd
import numpy as np

app = Flask(__name__)

# ==========================================
# HOME ROUTE (FIXES NOT FOUND ERROR)
# ==========================================
@app.route("/")
def home():
    return "🚀 Crime ML Flask Server Running Successfully"

# ==========================================
# ML RESULTS API
# ==========================================
@app.route("/ml_results")
def ml_results():

    # FETCH DATA FROM PHP BACKEND
    url = "http://localhost/Chronology/fetch_data.php"
    res = requests.get(url)
    data = res.json()

    # SAFE DATA HANDLING
    df = pd.DataFrame(data)
    df.columns = df.columns.str.lower()

    # STANDARDIZE COLUMN NAMES
    df = df.rename(columns={
        "location": "location",
        "locations": "location",
        "count": "crime_count",
        "counts": "crime_count"
    })

    # FORCE NUMERIC CLEANING
    df['crime_count'] = pd.to_numeric(df['crime_count'], errors='coerce')
    df = df.dropna(subset=['crime_count'])

    # CONVERT TO FLOAT
    df['crime_count'] = df['crime_count'].astype(float)

    # ==============================
    # SIMPLE ML LOGIC (RISK CLASS)
    # ==============================
    threshold = df['crime_count'].mean()
    df['risk'] = (df['crime_count'] > threshold).astype(int)

    # OUTPUT SUMMARY
    return jsonify({
        "total_locations": int(len(df)),
        "high_risk": int(df['risk'].sum()),
        "low_risk": int(len(df) - df['risk'].sum())
    })

# ==========================================
# RUN SERVER
# ==========================================
if __name__ == "__main__":
    app.run(debug=True)