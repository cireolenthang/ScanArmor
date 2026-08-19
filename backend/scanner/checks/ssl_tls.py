import socket
import ssl
from datetime import datetime


def _get_cert(hostname, port=443, timeout=5):
    context = ssl.create_default_context()
    conn = socket.create_connection((hostname, port), timeout=timeout)
    sock = context.wrap_socket(conn, server_hostname=hostname)
    try:
        cert = sock.getpeercert()
        return cert
    finally:
        try:
            sock.close()
        except Exception:
            pass


def run(target_url):
    # extract hostname
    issues = []
    try:
        # naive extraction
        if '://' in target_url:
            hostname = target_url.split('://', 1)[1].split('/', 1)[0]
        else:
            hostname = target_url.split('/', 1)[0]

        cert = _get_cert(hostname)
        if not cert:
            issues.append({
                "title": "No valid TLS certificate",
                "detail": "Could not retrieve a TLS certificate for the host.",
                "severity": "critical",
                "check": "ssl_tls"
            })
            return issues

        # check expiry
        notAfter = cert.get('notAfter')
        if notAfter:
            expiry = datetime.strptime(notAfter, "%b %d %H:%M:%S %Y %Z")
            days_left = (expiry - datetime.utcnow()).days
            if days_left < 0:
                issues.append({
                    "title": "Expired TLS certificate",
                    "detail": f"Certificate expired {abs(days_left)} days ago.",
                    "severity": "critical",
                    "check": "ssl_tls"
                })
            elif days_left < 30:
                issues.append({
                    "title": "TLS certificate expiring soon",
                    "detail": f"Certificate will expire in {days_left} days.",
                    "severity": "high",
                    "check": "ssl_tls"
                })

        # protocol and cipher checks are complex; report basic info
        issues.append({
            "title": "TLS certificate present",
            "detail": "A TLS certificate was found and parsed (passive check).",
            "severity": "info",
            "check": "ssl_tls"
        })

    except Exception as e:
        issues.append({
            "title": "TLS check failed",
            "detail": str(e),
            "severity": "info",
            "check": "ssl_tls"
        })
    return issues
