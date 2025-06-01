# CTI-Harvesting-Pipeline

# ThreatFox Threat Intelligence Ingestion

A pipeline to pull recent ThreatFox IOCs and store them in a local SQL database for analysis.

## Setup

Clone this repo
```bash
git clone https://github.com/roy9495/CTI-Harvesting-Pipeline
cd threatfox-pipeline
```
Create a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

Install requirements
```bash
pip install -r requirements.txt
```
Create a profile in abuse.ch and generate a (API key)[https://auth.abuse.ch/] and paste it into .env 
```bash
.env → set the THREATFOX_API_KEY
```
config/settings.yaml → control DB path and days to fetch

Now Run
```bash
python scripts/init_db.py
python scripts/fetch_iocs.py
```

Add scripts/schedule.sh to the crontab for hourly sync.
