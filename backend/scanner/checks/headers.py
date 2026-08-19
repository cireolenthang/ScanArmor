import requests

REQUIRED_HEADERS = [
    ("Content-Security-Policy", 'high'),
    ("X-Frame-Options", 'medium'),
    ("X-Content-Type-Options", 'medium'),
    ("Strict-Transport-Security", 'high'),
    ("Referrer-Policy", 'low'),
    ("Permissions-Policy", 'low'),
]


def run(target_url):
    issues = []
    try:
        # Use GET because some headers are only present on full responses
        r = requests.get(target_url, timeout=10, allow_redirects=True)
        headers = {k.title(): v for k, v in r.headers.items()}

        for name, severity in REQUIRED_HEADERS:
            if name not in headers:
                issues.append({
                    "title": f"Missing header: {name}",
                    "detail": f"Response is missing the {name} header.",
                    "severity": severity,
                    "check": "headers"
                })

        # Simple CSP quality hint
        if 'Content-Security-Policy' in headers:
            csp = headers['Content-Security-Policy']
            if 'unsafe-inline' in csp:
                issues.append({
                    "title": "Weak CSP",
                    "detail": "CSP allows 'unsafe-inline', which weakens protections.",
                    "severity": "medium",
                    "check": "headers"
                })

    except requests.RequestException as e:
        issues.append({
            "title": "Header check failed",
            "detail": str(e),
            "severity": "info",
            "check": "headers"
        })
    return issues
