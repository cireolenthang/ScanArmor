import os

os.environ["REDIS_PROTOCOL"] = "2"

from celery import Celery
import json
from backend.scanner.orchestrator import run_all_checks
from backend.models import SessionLocal, Scan
CELERY_BROKER = os.environ.get("CELERY_BROKER", "redis://redis:6379/0")
CELERY_BACKEND = os.environ.get("CELERY_BACKEND", "redis://redis:6379/1")

celery_app = Celery("tasks", broker="redis://127.0.0.1:6379/0", backend="redis://127.0.0.1:6379/0")

celery_app.conf.update(
    broker_transport_options={'protocol_version': 2},
    result_backend_transport_options={'protocol_version': 2},
)

@celery_app.task(bind=True)
def enqueue_scan(self, scan_id: str, target_url: str):
    # Run the orchestrator (this function should be CPU/light IO safe)
    result = run_all_checks(target_url)

    # Persist result to DB
    db = SessionLocal()
    try:
        scan = db.query(Scan).filter(Scan.id == scan_id).first()
        if scan:
            scan.status = 'completed'
            scan.results = result
            scan.results = json.dumps(result) if isinstance(result, dict) else result
            db.add(scan)
            db.commit()
    finally:
        db.close()
    return result
