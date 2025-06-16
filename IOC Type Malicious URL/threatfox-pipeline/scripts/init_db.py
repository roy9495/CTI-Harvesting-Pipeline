import sqlite3
import os
import yaml

with open('config/settings.yaml') as f:
    config = yaml.safe_load(f)

os.makedirs(os.path.dirname(config['database_path']), exist_ok=True)
conn = sqlite3.connect(config['database_path'])

cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS threatfox_iocs (
    id INTEGER PRIMARY KEY,
    ioc TEXT,
    threat_type TEXT,
    threat_type_desc TEXT,
    ioc_type TEXT,
    ioc_type_desc TEXT,
    malware TEXT,
    malware_printable TEXT,
    malware_alias TEXT,
    malware_malpedia TEXT,
    confidence_level INTEGER,
    first_seen TEXT,
    last_seen TEXT,
    reporter TEXT,
    reference TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS ioc_tags (
    ioc_id INTEGER,
    tag TEXT,
    FOREIGN KEY (ioc_id) REFERENCES threatfox_iocs(id)
)
''')

conn.commit()
conn.close()
print("[+] Database schema created.")