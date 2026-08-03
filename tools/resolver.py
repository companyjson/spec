#!/usr/bin/env python3
"""companyjson-resolve: reference resolver for the company.json v0.1 spec.

Given a domain, produces the best available organization profile using the
fallback chain:

    1. company.json   (first-party canonical, spec §10-§11)
    2. Schema.org Organization JSON-LD embedded in the homepage
    3. Homepage meta-tag extraction (og:site_name, description, og:image)

Output labels every result with its source and, for company.json, its binding
result (direct | host-authorized-redirect | none) per spec §11, and evaluates
relationship reciprocity per §9.10.2.

Usage:
    resolver.py example.com [--json] [--no-mutual]
                [--map logical_host=http://localhost:PORT]  (testing only)
                [--schema PATH] [--max-redirects N]

--map substitutes the transport for a logical host so the spec logic
(host binding, HTTPS rules) can be tested against local servers. Binding is
always evaluated against LOGICAL URLs, never the mapped transport.
"""
import argparse, json, re, sys, urllib.request, urllib.parse, urllib.error
from html.parser import HTMLParser

try:
    from jsonschema import Draft202012Validator
except ImportError:
    Draft202012Validator = None

MAX_BYTES = 1_048_576  # spec §7.2
UA = "companyjson-resolver/0.1 (+https://companyjson.org)"
SUPPORTED_SPEC_VERSION = "0.1"

# ---------------------------------------------------------------- utilities

def normalize_host(url_or_host):
    """Spec §11.1 host normalization. Returns normalized host or None.

    Step 6 says to ignore the *default* port for the scheme, not every
    port -- a non-default port is preserved so example.com:8443 is not
    treated as equivalent to example.com.
    """
    s = url_or_host
    port_suffix = ""
    if "://" in s:
        p = urllib.parse.urlsplit(s)
        if p.scheme not in ("http", "https"):
            return None
        host = p.hostname or ""
        try:
            port = p.port
        except ValueError:
            port = None
        default_port = 80 if p.scheme == "http" else 443
        if port is not None and port != default_port:
            port_suffix = f":{port}"
    else:
        host = s
    try:
        host = host.encode("idna").decode("ascii")  # step 2: domain-to-ASCII
    except (UnicodeError, AttributeError):
        pass
    host = host.lower().rstrip(".")                 # steps 3-4
    if host.startswith("www."):                     # step 5
        host = host[4:]
    return (host + port_suffix) if host else None


class _Fetcher:
    """Manual redirect-following fetcher that records the chain and applies
    --map transport substitution while evaluating spec rules on logical URLs."""

    def __init__(self, host_map, max_redirects=5, timeout=10):
        self.host_map = host_map or {}
        self.max_redirects = max_redirects
        self.timeout = timeout

    def _transport(self, logical_url):
        p = urllib.parse.urlsplit(logical_url)
        base = self.host_map.get(p.hostname)
        if base:
            b = urllib.parse.urlsplit(base)
            return urllib.parse.urlunsplit((b.scheme, b.netloc, p.path, p.query, ""))
        return logical_url

    def fetch(self, url):
        """Returns dict: status, body(bytes)|None, chain(list of logical URLs),
        final_url(logical), error, insecure_hop(bool: any non-https logical URL
        in chain), content_type."""
        chain, current = [url], url
        insecure = urllib.parse.urlsplit(url).scheme != "https"
        for _ in range(self.max_redirects + 1):
            req = urllib.request.Request(self._transport(current), headers={"User-Agent": UA})
            opener = urllib.request.build_opener(_NoRedirect())
            try:
                resp = opener.open(req, timeout=self.timeout)
                body = resp.read(MAX_BYTES + 1)
                if len(body) > MAX_BYTES:
                    return dict(status=None, body=None, chain=chain, final_url=current,
                                error="exceeds 1 MiB consumer limit (spec §7.2)",
                                insecure_hop=insecure, content_type=None)
                return dict(status=resp.status, body=body, chain=chain, final_url=current,
                            error=None, insecure_hop=insecure,
                            content_type=resp.headers.get("Content-Type", ""))
            except urllib.error.HTTPError as e:
                if e.code in (301, 302, 303, 307, 308):
                    loc = e.headers.get("Location")
                    if not loc:
                        return dict(status=e.code, body=None, chain=chain, final_url=current,
                                    error="redirect without Location", insecure_hop=insecure,
                                    content_type=None)
                    nxt = urllib.parse.urljoin(current, loc)
                    if urllib.parse.urlsplit(nxt).scheme != "https":
                        insecure = True                      # §10.1 / §11.3
                    chain.append(nxt)
                    current = nxt
                    continue
                return dict(status=e.code, body=None, chain=chain, final_url=current,
                            error=f"HTTP {e.code}", insecure_hop=insecure, content_type=None)
            except Exception as e:
                return dict(status=None, body=None, chain=chain, final_url=current,
                            error=str(e), insecure_hop=insecure, content_type=None)
        return dict(status=None, body=None, chain=chain, final_url=current,
                    error="redirect limit exceeded", insecure_hop=insecure, content_type=None)


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **kw):
        return None

# ------------------------------------------------------- binding (spec §11)

def evaluate_binding(fetch_result, declared_url, discovery_path="/company.json"):
    """Returns (binding, notes[]). binding in {'direct','host-authorized-redirect','none'}."""
    notes = []
    declared = normalize_host(declared_url or "")
    if not declared:
        return "none", ["declared url missing or unparseable"]
    initial, final = fetch_result["chain"][0], fetch_result["final_url"]
    init_p, final_p = urllib.parse.urlsplit(initial), urllib.parse.urlsplit(final)
    init_host, final_host = normalize_host(initial), normalize_host(final)

    if final_host == declared:                               # §11.2 direct
        if final_p.scheme != "https":
            notes.append("insecure transport (HTTP) — reported per §11.2")
        return "direct", notes

    # §11.3 host-authorized redirect: 8 conditions
    cond = {
        "initial HTTPS": init_p.scheme == "https",
        "discovery path": init_p.path == discovery_path,
        "initial host = declared host": init_host == declared,
        "redirect occurred": len(fetch_result["chain"]) > 1,
        "all hops HTTPS": not fetch_result["insecure_hop"],
        "profile declared host = initial host": True,        # caller checked declared==?; recheck:
    }
    cond["profile declared host = initial host"] = (declared == init_host)
    failed = [k for k, v in cond.items() if not v]
    if not failed:
        return "host-authorized-redirect", notes
    notes.append("redirect authorization failed: " + "; ".join(failed))
    return "none", notes

# ------------------------------------------------- fallback extractors

class _LDExtract(HTMLParser):
    def __init__(self):
        super().__init__(); self.in_ld = False; self.blocks = []; self.meta = {}
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "script" and a.get("type", "").lower() == "application/ld+json":
            self.in_ld = True; self._buf = []
        if tag == "meta":
            key = a.get("property") or a.get("name")
            if key and a.get("content"):
                self.meta[key.lower()] = a["content"]
    def handle_endtag(self, tag):
        if tag == "script" and self.in_ld:
            self.in_ld = False; self.blocks.append("".join(self._buf))
    def handle_data(self, d):
        if self.in_ld: self._buf.append(d)


def _find_org(node):
    if isinstance(node, list):
        for x in node:
            r = _find_org(x)
            if r: return r
    elif isinstance(node, dict):
        t = node.get("@type", "")
        types = t if isinstance(t, list) else [t]
        if any(isinstance(x, str) and x.endswith("Organization") for x in types):
            return node
        for v in node.values():
            r = _find_org(v)
            if r: return r
    return None


def extract_fallback(homepage_bytes):
    """Returns (profile_dict, source) from JSON-LD or meta tags, else (None, None)."""
    try:
        html = homepage_bytes.decode("utf-8", errors="replace")
    except Exception:
        return None, None
    p = _LDExtract()
    try:
        p.feed(html)
    except Exception:
        pass
    for block in p.blocks:
        try:
            org = _find_org(json.loads(block.strip()))
        except Exception:
            continue
        if org:
            prof = {k: org.get(sk) for k, sk in
                    [("name", "name"), ("legalName", "legalName"), ("url", "url"),
                     ("description", "description"), ("sameAs", "sameAs")]}
            logo = org.get("logo")
            prof["logo"] = logo.get("url") if isinstance(logo, dict) else logo
            return {k: v for k, v in prof.items() if v}, "structured-data (Schema.org JSON-LD)"
    m = p.meta
    prof = {"name": m.get("og:site_name") or m.get("og:title"),
            "description": m.get("og:description") or m.get("description"),
            "logo": m.get("og:image"),
            "url": m.get("og:url")}
    prof = {k: v for k, v in prof.items() if v}
    return (prof, "inferred (page extraction)") if prof.get("name") else (None, None)

# ------------------------------------------------- reciprocity (spec §9.10.2)

RECIPROCAL = {"parentOrganization": {"subOrganization", "brand"},
              "subOrganization": {"parentOrganization"},
              "brand": {"parentOrganization"},
              "memberOf": {"member"}, "member": {"memberOf"},
              "affiliate": {"affiliate"}}


def evaluate_mutual(rel, origin_declared_host, fetcher, validator):
    if "profile" not in rel:
        return "declared", "no profile URL to check"
    if rel.get("url"):
        url_host = normalize_host(rel["url"])
        profile_host = normalize_host(rel["profile"])
        if url_host and profile_host and url_host != profile_host:
            # The relationship's own url and profile disagree about which
            # host they name. Trusting profile here would let a relationship
            # link one entity (url) while proving reciprocity against an
            # unrelated document (profile) fetched from a different host --
            # refuse rather than silently evaluate the wrong entity.
            return ("unavailable",
                    f"declared profile host ({profile_host!r}) does not "
                    f"match declared url host ({url_host!r})")
    r = fetcher.fetch(rel["profile"])
    if r["error"] or r["status"] != 200 or not r["body"]:
        return "unavailable", r["error"] or f"HTTP {r['status']}"
    try:
        counter = json.loads(r["body"].decode("utf-8"))
    except Exception as e:
        return "unavailable", f"invalid JSON: {e}"
    if validator and list(validator.iter_errors(counter)):
        return "unavailable", "counterpart fails schema validation"
    binding, _ = evaluate_binding(r, counter.get("url"))
    if binding == "none":
        return "unavailable", "counterpart not first-party-bound (§9.10.2 cond. 4)"
    compatible = RECIPROCAL.get(rel.get("type"), set())
    found_conflict = False
    for cr in counter.get("relationships", []):
        hosts = {normalize_host(cr[k]) for k in ("url", "profile") if cr.get(k)}
        if origin_declared_host in hosts:
            if cr.get("type") in compatible:
                return "mutually-declared", f"counterpart declares {cr.get('type')}"
            found_conflict = True
    return ("conflicting", "counterpart declares incompatible type") if found_conflict \
        else ("declared", "no reciprocal declaration found")

# --------------------------------------------------------------- resolve

def resolve(domain, fetcher, validator, check_mutual=True, discovery_path="/company.json"):
    out = {"input": domain, "profile": None, "source": None, "binding": None,
           "valid": None, "validation_errors": [], "notes": [], "relationships": []}
    domain = domain.strip().rstrip("/")
    if "://" not in domain:
        domain = "https://" + domain
    host = urllib.parse.urlsplit(domain).hostname

    # 1) company.json
    disc_url = f"https://{host}{discovery_path}"
    r = fetcher.fetch(disc_url)
    if not r["error"] and r["status"] == 200 and r["body"]:
        try:
            doc = json.loads(r["body"].decode("utf-8"))
        except Exception as e:
            out["notes"].append(f"company.json present but unparseable ({e}); falling back")
            doc = None
        if isinstance(doc, dict):
            out["profile"], out["source"] = doc, "first-party (company.json)"
            out["specVersion"] = doc.get("specVersion")
            if out["specVersion"] != SUPPORTED_SPEC_VERSION:
                # Spec §12.1: report as an unsupported version, not as
                # invalid -- a document must not be treated as malformed
                # solely because this resolver lacks its matching schema.
                out["notes"].append(
                    f"unsupported specVersion {out['specVersion']!r}; this "
                    f"resolver only validates {SUPPORTED_SPEC_VERSION!r} "
                    "(spec §12.1) -- not evaluated as invalid solely for that reason"
                )
            elif validator:
                errs = [f"{e.json_path}: {e.message}" for e in validator.iter_errors(doc)]
                out["valid"], out["validation_errors"] = not errs, errs
            out["binding"], notes = evaluate_binding(r, doc.get("url"), discovery_path)
            out["notes"] += notes
            if out["binding"] == "none":
                out["source"] = "third-party declaration (company.json, NOT first-party-bound)"
            if check_mutual:
                origin_host = normalize_host(doc.get("url") or "")
                for rel in doc.get("relationships", []):
                    status, why = evaluate_mutual(rel, origin_host, fetcher, validator)
                    out["relationships"].append(
                        {"type": rel.get("type"), "name": rel.get("name"),
                         "status": status, "detail": why})
            return out
    else:
        out["notes"].append(f"no company.json at {disc_url} ({r['error'] or 'HTTP '+str(r['status'])})")

    # 2-3) homepage fallbacks
    hp = fetcher.fetch(f"https://{host}/")
    if hp["body"]:
        prof, source = extract_fallback(hp["body"])
        if prof:
            out["profile"], out["source"], out["binding"] = prof, source, "n/a (not company.json)"
            return out
    out["notes"].append("no extractable organization data found")
    return out

# ----------------------------------------------------------------- CLI

def main():
    ap = argparse.ArgumentParser(description="company.json reference resolver")
    ap.add_argument("domain")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    ap.add_argument("--no-mutual", action="store_true")
    ap.add_argument("--schema", default=None)
    ap.add_argument("--max-redirects", type=int, default=5)
    ap.add_argument("--map", action="append", default=[],
                    help="logical_host=transport_base (testing only)")
    a = ap.parse_args()

    host_map = {}
    for m in a.map:
        k, _, v = m.partition("=")
        host_map[k] = v
    validator = None
    if a.schema and Draft202012Validator:
        validator = Draft202012Validator(json.load(open(a.schema)))

    fetcher = _Fetcher(host_map, a.max_redirects)
    res = resolve(a.domain, fetcher, validator, check_mutual=not a.no_mutual)

    if a.json:
        print(json.dumps(res, indent=2)); return

    p = res["profile"] or {}
    print(f"\n  {p.get('name', '(no name found)')}")
    if p.get("description"): print(f"  {p['description']}")
    print(f"\n  Source:   {res['source'] or 'none'}")
    if res["binding"]: print(f"  Binding:  {res['binding']}")
    if res.get("specVersion") not in (None, SUPPORTED_SPEC_VERSION):
        print(f"  Schema:   unsupported specVersion {res['specVersion']!r}")
    elif res["valid"] is not None:
        print(f"  Schema:   {'valid' if res['valid'] else 'INVALID'}")
        for e in res["validation_errors"]: print(f"            - {e}")
    for k in ("url", "legalName", "logo"):
        if p.get(k): print(f"  {k}: {p[k]}")
    if p.get("sameAs"): print(f"  sameAs: {', '.join(p['sameAs'][:5])}")
    for rel in res["relationships"]:
        print(f"  Relationship: {rel['type']} -> {rel['name']}: "
              f"{rel['status'].upper()} ({rel['detail']})")
    for n in res["notes"]: print(f"  note: {n}")
    print()

if __name__ == "__main__":
    main()
