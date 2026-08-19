# SMB Shield

SMB Shield is a lightweight open-source web security scanner aimed at small and medium-sized businesses. It checks websites for common misconfigurations and security issues and presents findings in plain language with actionable remediation advice.

![screenshot-placeholder](screenshot.png)

## Quick start (Docker)

1. docker-compose build
2. docker-compose up -d
3. Open http://localhost:3000

## What it checks

- HTTP Security Headers (CSP, HSTS, X-Frame-Options, X-Content-Type-Options, Referrer-Policy, Permissions-Policy)
- SSL/TLS certificate validity and expiry
- DNS records (SPF, DMARC) and passive subdomain discovery via crt.sh
- (More checks planned: ports, CMS detection, cookies, CORS, rate limits, robots.txt)

## How to add a new check module

Checks live under `backend/scanner/checks/`. Each check should implement a `run(target_url: str) -> list` function that returns a list of issue dicts with keys: `title`, `detail`, `severity` (critical/high/medium/low/info), and `check`.

To add a check:
1. Create `backend/scanner/checks/your_check.py` with a `run` function.
2. Import it in `backend/scanner/orchestrator.py` and add the function to the `checks` list.
3. The orchestrator will run checks in parallel and aggregate results.

## Roadmap

- Implement remaining checks (ports, CMS detection, cookies, CORS, robots)
- PDF export with branded templates
- User accounts and authenticated history
- Hosted free option with rate limits and abuse protections

## License

MIT
