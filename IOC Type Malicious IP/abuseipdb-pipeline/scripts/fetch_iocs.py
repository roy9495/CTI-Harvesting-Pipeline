import os
import yaml
import sqlite3
import requests
from dotenv import load_dotenv
from datetime import datetime

# Load API key
load_dotenv()
API_KEY = os.getenv("ABUSEIPDB_API_KEY")

# Load config
with open("config/settings.yaml") as f:
    config = yaml.safe_load(f)

DB_PATH = config["database_path"]
CONFIDENCE_MIN = config.get("confidence_minimum", 80)
LIMIT = config.get("limit", 10000)

# Ensure DB directory exists
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

# AbuseIPDB API request
print(f"[+] Requesting AbuseIPDB blacklist (≥{CONFIDENCE_MIN}, max {LIMIT})")
url = "https://api.abuseipdb.com/api/v2/blacklist"
headers = {
    "Key": API_KEY,
    "Accept": "application/json"
}
params = {
    "confidenceMinimum": CONFIDENCE_MIN,
    "limit": LIMIT
}
response = requests.get(url, headers=headers, params=params)

if response.status_code != 200:
    print(f"[-] API request failed: {response.status_code}")
    print(response.text)
    exit(1)

data = response.json().get("data", [])
print(f"[+] Received {len(data)} IPs")

# Insert into SQLite
conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.execute('''
CREATE TABLE IF NOT EXISTS abuseipdb_blacklist (
    ip_address TEXT PRIMARY KEY,
    abuse_confidence_score INTEGER,
    country_code TEXT,
    last_reported_at TEXT,
    inserted_at TEXT DEFAULT CURRENT_TIMESTAMP
)
''')

for entry in data:
    cur.execute('''
        INSERT OR REPLACE INTO abuseipdb_blacklist (
            ip_address, abuse_confidence_score, country_code, last_reported_at
        ) VALUES (?, ?, ?, ?)
    ''', (
        entry["ipAddress"],
        entry["abuseConfidenceScore"],
        entry["countryCode"],
        entry.get("lastReportedAt", "")
    ))

conn.commit()
conn.close()
print(f"[+] Stored in SQLite DB: {DB_PATH}")

