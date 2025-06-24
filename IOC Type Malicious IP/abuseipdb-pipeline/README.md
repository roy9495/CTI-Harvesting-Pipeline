# ThreatFox Threat Intelligence Ingestion

A pipeline to pull recent ThreatFox IOCs and store them in a local SQL database for analysis.

## Setup

Clone this repo
```bash
git clone https://github.com/roy9495/CTI-Harvesting-Pipeline
cd abuseipdb-pipeline
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
Create a profile in abuse.ch and generate a [API key](https://www.abuseipdb.com/) and paste it into .env 
```bash
.env → set the abusepdb_api_key
```
config/settings.yaml → control DB path and days to fetch

Now Run
```bash
python scripts/fetch_iocs.py
```
## Cronjob
Add scripts/schedule.sh to the crontab for data sync.

To know the OS
```bash
cat /etc/os-release
```
For Debian / Ubuntu / Kali / Parrot
```bash
sudo apt update
sudo apt install cron
```
For Red Hat / CentOS / Alma / Rocky / Fedora
```bash
sudo yum install cronie
```
To verify if CRON is installed
```bash
which crontab
```
Now we have to create a logs directory
```bash
mkdir -p logs
```
And create a fetch.log file inside it

Now make the schedule.sh script executable
```bash
chmod +x scripts/schedule.sh
```
Now to run the CRON job every 1 minute and  fetch the IOCs we have have open the CRON tab
```bash
crontab -e
```
And add this line to the end of the file
```bash
* * * * * /path_to/CTI-Harvesting-Pipeline/abuseipdb-pipeline/scripts/schedule.sh
```
Now we have to restart the CRON service
```bash
sudo service cron restart
```
## CRON JOBS FOR VARIOUS INTERVALS

Every 5 minutes
```bash
*/5 * * * * /path_to/CTI-Harvesting-Pipeline/abuseipdb-pipeline/scripts/schedule.sh
```

Every 10 minutes
```bash
*/10 * * * * /path_to/CTI-Harvesting-Pipeline/abuseipdb-pipeline/scripts/schedule.sh
```

Every 15 minutes
```bash
*/15 * * * * /path_to/CTI-Harvesting-Pipeline/abuseipdb-pipeline/scripts/schedule.sh
```

Every 30 minutes

```bash
*/30 * * * * /path_to/CTI-Harvesting-Pipeline/abuseipdb-pipeline/scripts/schedule.sh
```

Every 1 hour
```bash
0 * * * * /path_to/CTI-Harvesting-Pipeline/abuseipdb-pipeline/scripts/schedule.sh
```
