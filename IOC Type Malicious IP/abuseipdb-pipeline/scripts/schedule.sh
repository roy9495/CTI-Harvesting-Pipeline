#!/bin/bash
cd "$(dirname "$0")/.."
source venv/bin/activate
python scripts/fetch_iocs.py >> logs/fetch.log 2>&1