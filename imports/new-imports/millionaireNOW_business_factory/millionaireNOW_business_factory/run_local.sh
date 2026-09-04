#!/usr/bin/env bash
set -e
python -m uvicorn 01_match_market.app:app --host 0.0.0.0 --port 8101 &
python -m uvicorn 02_verified_compare.app:app --host 0.0.0.0 --port 8102 &
python -m uvicorn 03_ai_site_audit.app:app --host 0.0.0.0 --port 8103 &
python -m uvicorn 04_premium_advisor_store.app:app --host 0.0.0.0 --port 8104 &
python -m uvicorn 05_outbound_engine.app:app --host 0.0.0.0 --port 8105 &
wait
