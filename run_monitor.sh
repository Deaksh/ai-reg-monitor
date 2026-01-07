#!/bin/bash
cd /Users/deakshshetty/Documents/ai_reg_monitor
source .venv/bin/activate
python run_once.py >> monitor.log 2>&1
