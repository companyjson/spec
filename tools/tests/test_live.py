#!/usr/bin/env python3
"""Live integration tests for company.json reference implementations.

Two modes:
  --capture   Fetch live profiles from systemthree.com and mtncoat.com,
              save them as local fixtures in fixtures/, and run assertions.
  (default)   Run assertions against saved fixtures (no network required).

CI usage:
  Local fixture suite (every push):    python3 test_live.py
  Live integration (daily cron):       python3 test_live.py --capture
"""
import argparse, json, os, sys, urllib.request

FIXTURE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures")

SITES = {
    "systemthree": {
        "domain": "systemthree.com",
        "discovery": "https://www.systemthree.com/company.json",
        "expect": {
            "name": "System Three Resins",
            "url": "https://www.systemthree.com/",
            "specVersion": "0.1",
            "relationship_type": "brand",
            "relationship_name": "MTN Coat",
        }
    },
    "mtncoat": {
        "domain": "mtncoat.com",
        "discovery": "https://mtncoat.com/company.json",
        "expect": {
            "name": "MTN Coat",
            "url": "https://mtncoat.com/",
            "specVersion": "0.1",
            "relationship_type": "parentOrganization",
            "relationship_name": "System Three Resins",
        }
    }
}

# ---------------------------------------------------------------- fetch / fixture

def fetch_live(url):
    """Follow redirects, return (final_url, body_bytes, redirect_chain)."""
    opener = urllib.request.build_opener()
    req = urllib.request.Request(url, headers={"User-Agent": "companyjson-test/0.1"})
    resp = opener.open(req, timeout=15)
    return resp.url, resp.read(), resp.status

def save_fixture(key, body, meta):
    os.makedirs(FIXTURE_DIR, exist_ok=True)
    with open(os.path.join(FIXTURE_DIR, f"{key}.json"), "wb") as f:
        f.write(body)
    with open(os.path.join(FIXTURE_DIR, f"{key}.meta.json"), "w") as f:
        json.dump(meta, f, indent=2)

def load_fixture(key):
    with open(os.path.join(FIXTURE_DIR, f"{key}.json"), "rb") as f:
        body = f.read()
    with open(os.path.join(FIXTURE_DIR, f"{key}.meta.json")) as f:
        meta = json.load(f)
    return body, meta

# ---------------------------------------------------------------- assertions

ok = True
def check(label, condition, detail=""):
    global ok
    status = "PASS" if condition else "FAIL"
    msg = f"{status}  {label}"
    if not condition and detail:
        msg += f"  [{detail}]"
    print(msg)
    ok = ok and condition

def run_assertions(key, body, meta, site):
    exp = site["expect"]
    try:
        doc = json.loads(body)
    except Exception as e:
        check(f"{key}: valid JSON", False, str(e))
        return

    check(f"{key}: valid JSON", True)
    check(f"{key}: specVersion", doc.get("specVersion") == exp["specVersion"],
          f"got {doc.get('specVersion')}")
    check(f"{key}: name", doc.get("name") == exp["name"],
          f"got {doc.get('name')}")
    check(f"{key}: url", doc.get("url") == exp["url"],
          f"got {doc.get('url')}")
    check(f"{key}: has relationships", bool(doc.get("relationships")))

    rels = doc.get("relationships", [])
    match = [r for r in rels if r.get("type") == exp["relationship_type"]
             and r.get("name") == exp["relationship_name"]]
    check(f"{key}: expected relationship present", len(match) == 1,
          f"looking for {exp['relationship_type']} -> {exp['relationship_name']}")

    if match:
        check(f"{key}: relationship has profile URL", bool(match[0].get("profile")))

    # Redirect-authorization checks (live mode only)
    if meta.get("final_url"):
        from urllib.parse import urlsplit
        initial_host = urlsplit(site["discovery"]).hostname
        final_host = urlsplit(meta["final_url"]).hostname
        was_redirected = initial_host != final_host
        check(f"{key}: host-authorized-redirect (redirected to CDN)",
              was_redirected,
              f"initial={initial_host} final={final_host}")
        check(f"{key}: final URL is HTTPS",
              urlsplit(meta["final_url"]).scheme == "https")

def run_mutual_declaration(profiles):
    """Cross-check that both profiles declare each other correctly."""
    st = profiles.get("systemthree")
    mtn = profiles.get("mtncoat")
    if not st or not mtn:
        check("mutual declaration: both profiles loaded", False)
        return

    # System Three declares brand -> MTN Coat
    st_rels = st.get("relationships", [])
    st_to_mtn = [r for r in st_rels
                 if r.get("type") == "brand" and r.get("name") == "MTN Coat"]
    check("mutual: ST declares brand -> MTN Coat", len(st_to_mtn) == 1)

    # MTN Coat declares parentOrganization -> System Three Resins
    mtn_rels = mtn.get("relationships", [])
    mtn_to_st = [r for r in mtn_rels
                 if r.get("type") == "parentOrganization"
                 and r.get("name") == "System Three Resins"]
    check("mutual: MTN declares parentOrganization -> ST", len(mtn_to_st) == 1)

    # Both have profile URLs pointing at each other's domains
    if st_to_mtn:
        profile_url = st_to_mtn[0].get("profile", "")
        check("mutual: ST->MTN profile points to mtncoat.com",
              "mtncoat.com" in profile_url, profile_url)
    if mtn_to_st:
        profile_url = mtn_to_st[0].get("profile", "")
        check("mutual: MTN->ST profile points to systemthree.com",
              "systemthree.com" in profile_url, profile_url)

    # Reciprocal types are compatible per §9.10.1
    check("mutual: relationship types are compatible reciprocals (brand <-> parentOrganization)",
          len(st_to_mtn) == 1 and len(mtn_to_st) == 1)

# ---------------------------------------------------------------- main

def main():
    global ok
    ap = argparse.ArgumentParser()
    ap.add_argument("--capture", action="store_true",
                    help="Fetch live profiles and save as fixtures")
    args = ap.parse_args()

    profiles = {}
    for key, site in SITES.items():
        if args.capture:
            print(f"\nFetching {site['discovery']} ...")
            try:
                final_url, body, status = fetch_live(site["discovery"])
                meta = {"final_url": final_url, "status": status,
                        "discovery_url": site["discovery"]}
                save_fixture(key, body, meta)
                print(f"  -> saved fixture ({len(body)} bytes, final: {final_url})")
            except Exception as e:
                check(f"{key}: fetch", False, str(e))
                continue
        else:
            try:
                body, meta = load_fixture(key)
            except FileNotFoundError:
                print(f"No fixture for {key}. Run with --capture first.")
                sys.exit(1)

        run_assertions(key, body, meta, site)
        try:
            profiles[key] = json.loads(body)
        except Exception:
            pass

    print()
    run_mutual_declaration(profiles)

    print(f"\n{'ALL TESTS PASS' if ok else 'FAILURES PRESENT'}")
    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()
