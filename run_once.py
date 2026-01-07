#!/usr/bin/env python3
"""
ai_reg_monitor - GDPR Article 32 change detector
Monitors for updates and dispatches alerts.
"""

import json
import os
from scraper import fetch_article
from chunker import chunk_paragraphs
from change_detector import detect_changes
from classifier import classify_change
from impact import assess_impact
from alert_payload import build_alert_payload
from alert_dispatcher import dispatch_alert
from audit import log_event
from db import init_db, get_conn
from datetime import datetime
import json


VERSION_FILE = "gdpr_art32_latest.json"
ARTICLE_NAME = "GDPR Article 32"


def main():
    first_run = not os.path.exists(VERSION_FILE)

    # Load previous version (if exists)
    if not first_run:
        with open(VERSION_FILE, "r", encoding="utf-8") as f:
            old_paras = json.load(f)
        print(f"Loaded old version: {len(old_paras)} paragraphs")
    else:
        old_paras = []
        print("First run detected – no alerts will be sent")

    # Fetch latest content
    new_paras = fetch_article()
    print(f"Fetched new: {len(new_paras)} paragraphs")

    # First run → create baseline only
    if first_run:
        save_baseline(new_paras)
        return

    # Chunking
    old_chunks = chunk_paragraphs(old_paras)
    new_chunks = chunk_paragraphs(new_paras)

    print(f"Chunks old: {len(old_chunks)}, new: {len(new_chunks)}")

    # Change detection
    changes = detect_changes(old_chunks, new_chunks)
    print(f"Detected {len(changes)} changes")

    if not changes:
        print("No changes detected")
        save_baseline(new_paras)
        return

    # Process each detected change
    for ch in changes:
        # Classify change
        classification = classify_change(
            ch.get("before", ""),
            ch.get("after", "")
        )

        change_result = {
            "article": ARTICLE_NAME,
            "chunk_id": ch["chunk_id"],
            "change_kind": ch.get("change_kind", "MODIFIED"),
            "change_type": classification.change_type,
            "summary": classification.summary,
            "confidence": classification.confidence,
            "before": ch.get("before", ""),
            "after": ch.get("after", "")
        }

        conn = get_conn()
        cur = conn.cursor()

        cur.execute("""
        INSERT INTO detected_changes
        (article, chunk_id, change_type, summary, confidence, before, after, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            ARTICLE_NAME,
            ch["chunk_id"],
            classification.change_type,
            classification.summary,
            classification.confidence,
            ch["before"],
            ch["after"],
            datetime.utcnow().isoformat()
        ))

        change_id = cur.lastrowid
        conn.commit()
        conn.close()

        log_event("CHANGE_CLASSIFIED", {"change_id": change_id})

        # Impact assessment
        impact_result = assess_impact(change_result)
        conn = get_conn()
        conn.execute("""
        INSERT INTO impact_assessments
        (change_id, applies, risk_level, recommended_action, reasoning, confidence, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            change_id,
            impact_result.applies,
            impact_result.risk_level,
            impact_result.recommended_action,
            json.dumps(impact_result.reasoning),
            impact_result.confidence,
            datetime.utcnow().isoformat()
        ))
        conn.commit()
        conn.close()

        log_event("IMPACT_ASSESSED", {"change_id": change_id})

        print(
            f"Impact → applies={impact_result.applies}, "
            f"risk={impact_result.risk_level}, "
            f"confidence={impact_result.confidence}"
        )

        # Alerting
        payload = build_alert_payload(change_result, impact_result)
        dispatch_alert(payload, impact_result)

        print(f"Processed change for chunk {ch['chunk_id']}")

    # Update baseline after successful run
    save_baseline(new_paras)
    print("Pipeline complete")


def save_baseline(paras):
    """Save current version as new baseline"""
    with open(VERSION_FILE, "w", encoding="utf-8") as f:
        json.dump(paras, f, ensure_ascii=False, indent=2)
    print(f"Baseline updated: {VERSION_FILE}")


if __name__ == "__main__":
    init_db()
    main()
