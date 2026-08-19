import concurrent.futures
from backend.scanner.checks import headers, ssl_tls, dns
from datetime import datetime

# Severity weights per project spec
SEVERITY_WEIGHTS = {
    "critical": -30,
    "high": -15,
    "medium": -8,
    "low": -3,
    "info": 0,
}

GRADE_MAP = [(90, 'A'), (75, 'B'), (60, 'C'), (40, 'D'), (0, 'F')]


def run_all_checks(target_url: str):
    """Run all enabled checks in parallel and aggregate results."""
    checks = [headers.run, ssl_tls.run, dns.run]
    findings = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=len(checks)) as ex:
        futures = [ex.submit(check, target_url) for check in checks]
        for f in concurrent.futures.as_completed(futures):
            try:
                res = f.result()
                if isinstance(res, list):
                    findings.extend(res)
            except Exception as e:
                findings.append({
                    "title": "Check failure",
                    "detail": str(e),
                    "severity": "info",
                    "check": "orchestrator"
                })

    # Calculate score
    score = 100
    for issue in findings:
        sev = issue.get('severity', 'info').lower()
        score += SEVERITY_WEIGHTS.get(sev, 0)
    score = max(0, min(100, score))

    grade = 'F'
    for threshold, g in GRADE_MAP:
        if score >= threshold:
            grade = g
            break

    result = {
        "target": target_url,
        "timestamp": datetime.utcnow().isoformat() + 'Z',
        "score": score,
        "grade": grade,
        "issues": findings,
    }
    return result
