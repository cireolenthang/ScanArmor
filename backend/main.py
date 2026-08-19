import os
import json
from uuid import uuid4
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel, HttpUrl

from backend.tasks import enqueue_scan
from backend.models import init_db, Scan, SessionLocal
from backend.reports.pdf_generator import generate_pdf_report

app = FastAPI(title="SMB Shield API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()

class ScanRequest(BaseModel):
    url: HttpUrl

@app.post("/api/scan")
async def submit_scan(req: ScanRequest):
    scan_id = str(uuid4())
    target_str = str(req.url)

    # Create DB record
    db = SessionLocal()
    try:
        scan = Scan(id=scan_id, target=target_str, status="pending")
        db.add(scan)
        db.commit()
    finally:
        db.close()

    # Enqueue background scan
    enqueue_scan.delay(scan_id, target_str)
    return {"scan_id": scan_id}

@app.get("/api/scan/{scan_id}")
async def get_scan(scan_id: str):
    db = SessionLocal()
    try:
        scan = db.query(Scan).filter(Scan.id == scan_id).first()
        if not scan:
            raise HTTPException(status_code=404, detail="Scan not found")

        # Safely parse JSON results if stored as a string in SQLite
        results_data = json.loads(scan.results) if isinstance(scan.results, str) else scan.results
        
        return {
            "id": scan.id,
            "target": scan.target,
            "status": scan.status,
            "results": results_data
        }
    finally:
        db.close()

@app.get("/api/scan/{scan_id}/pdf")
async def download_pdf_report(scan_id: str):
    db = SessionLocal()
    try:
        scan = db.query(Scan).filter(Scan.id == scan_id).first()
        if not scan or not scan.results:
            raise HTTPException(status_code=404, detail="Scan result not found")

        results = json.loads(scan.results) if isinstance(scan.results, str) else scan.results

        # Ensure temp directory exists
        os.makedirs("temp_reports", exist_ok=True)
        pdf_path = f"temp_reports/report_{scan_id}.pdf"

        # Generate PDF report
        generate_pdf_report(results, pdf_path)

        return FileResponse(
            pdf_path,
            media_type="application/pdf",
            filename=f"SMB_Shield_Report_{scan_id}.pdf"
        )
    finally:
        db.close()