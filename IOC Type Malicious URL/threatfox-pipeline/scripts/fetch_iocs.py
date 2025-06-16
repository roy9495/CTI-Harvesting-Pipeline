import os
import requests
import sqlite3
import yaml
from tqdm import tqdm
from dotenv import load_dotenv

load_dotenv()

with open('config/settings.yaml') as f:
    config = yaml.safe_load(f)

API_KEY = os.getenv("THREATFOX_API_KEY")
DB_PATH = config["database_path"]
LOG_FILE = config["log_file"]
DAYS = config["days_to_fetch"]

API_URL = 'https://threatfox-api.abuse.ch/api/v1/'

headers = {"Auth-Key": API_KEY}
payload = {
    "query": "get_iocs",
    "days": DAYS
}

resp = requests.post(API_URL, json=payload, headers=headers)
resp.raise_for_status()
data = resp.json()

if data.get("query_status") != "ok":
    print("[-] Invalid response from ThreatFox")
    exit()

iocs = data["data"]
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Fetch all existing IDs once
cursor.execute('SELECT id FROM threatfox_iocs')
existing_ids = set(row[0] for row in cursor.fetchall())

for ioc in tqdm(iocs):
    # Filter: Only allow ioc_type == "ip:port"
    if ioc.get('ioc_type') != "ip:port":
        continue  # Skip all other types

    ioc_id = int(ioc['id'])
    if ioc_id in existing_ids:
        continue  # Skip if already exists

    cursor.execute('''
        INSERT INTO threatfox_iocs (
            id, ioc, threat_type, threat_type_desc, ioc_type,
            ioc_type_desc, malware, malware_printable, malware_alias,
            malware_malpedia, confidence_level, first_seen, last_seen,
            reporter, reference
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        ioc_id,
        ioc['ioc'],
        ioc['threat_type'],
        ioc['threat_type_desc'],
        ioc['ioc_type'],
        ioc['ioc_type_desc'],
        ioc['malware'],
        ioc['malware_printable'],
        ioc.get('malware_alias'),
        ioc.get('malware_malpedia'),
        ioc['confidence_level'],
        ioc['first_seen'],
        ioc.get('last_seen'),
        ioc['reporter'],
        ioc.get('reference')
    ))

    for tag in ioc.get("tags") or []:
        cursor.execute('''
            INSERT INTO ioc_tags (ioc_id, tag) VALUES (?, ?)
        ''', (ioc_id, tag))

conn.commit()
conn.close()
print("[+] Fetched and stored ThreatFox IOCs.")