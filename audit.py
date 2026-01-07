import json
from datetime import datetime
from db import insert_audit

def log_event(event_type: str, payload: dict):
    insert_audit(event_type, payload)


