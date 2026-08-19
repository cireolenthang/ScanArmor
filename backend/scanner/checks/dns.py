import requests
import dns.resolver


def _has_spf(domain):
    try:
        answers = dns.resolver.resolve(domain, 'TXT')
        for r in answers:
            txt = ''.join(r.strings) if hasattr(r, 'strings') else str(r)
            if txt.startswith('v=spf1'):
                return True, txt
    except Exception:
        pass
    return False, None


def _has_dmarc(domain):
    try:
        answers = dns.resolver.resolve('_dmarc.' + domain, 'TXT')
        for r in answers:
            txt = ''.join(r.strings) if hasattr(r, 'strings') else str(r)
            if txt.startswith('v=DMARC1'):
                return True, txt
    except Exception:
        pass
    return False, None


def _crtsh_subs(domain):
    try:
        url = f"https://crt.sh/?q=%25.{domain}&output=json"
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            data = r.json()
            names = set()
            for item in data:
                name = item.get('name_value')
                if name:
                    for n in name.split('\n'):
                        names.add(n.strip())
            return list(names)
    except Exception:
        pass
    return []


def run(target_url):
    issues = []
    try:
        # extract domain
        if '://' in target_url:
            domain = target_url.split('://', 1)[1].split('/', 1)[0]
        else:
            domain = target_url.split('/', 1)[0]

        spf, spf_txt = _has_spf(domain)
        if not spf:
            issues.append({
                "title": "Missing SPF record",
                "detail": "No SPF (v=spf1) TXT record found for the domain.",
                "severity": "medium",
                "check": "dns"
            })

        dmarc, dmarc_txt = _has_dmarc(domain)
        if not dmarc:
            issues.append({
                "title": "Missing DMARC record",
                "detail": "No DMARC TXT record found for _dmarc.domain.",
                "severity": "low",
                "check": "dns"
            })

        subs = _crtsh_subs(domain)
        if subs:
            issues.append({
                "title": "Passive subdomain discovery",
                "detail": f"Found {len(subs)} certificate entries on crt.sh (passive).",
                "severity": "info",
                "check": "dns",
                "data": subs[:20]
            })

    except Exception as e:
        issues.append({
            "title": "DNS check failed",
            "detail": str(e),
            "severity": "info",
            "check": "dns"
        })
    return issues
