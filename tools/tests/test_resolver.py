#!/usr/bin/env python3
"""Negative-path regression tests for tools/resolver.py.

test_live.py proves the resolver works against two real, cooperating,
correctly-configured publishers. It does not exercise the failure paths
the specification spends most of its words on: a relationship declared
by only one side, a counterpart that can't be fetched, a counterpart
that declares an incompatible relationship type, binding failures
caused by an insecure redirect chain -- either starting over HTTP
(spec Sec 11.4) or downgrading to HTTP partway through (spec Sec 11.3
condition 5, distinct from Sec 11.4) -- a relationship whose own url
and profile fields disagree about which host they name, an unsupported
specVersion that must be reported as such rather than as generically
invalid (spec Sec 12.1), and host normalization that must discard only
the *default* port, not every port (spec Sec 11.1 step 6).

These are synthetic fixtures constructed in-process against
evaluate_binding() and evaluate_mutual() directly. No network access
is required and none of this depends on systemthree.com or mtncoat.com
staying online or unchanged.

Run:
    python3 test_resolver.py
"""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import resolver  # noqa: E402

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


# ---------------------------------------------------------------- fixtures

def fetch_result(chain, final_url=None, insecure_hop=False):
    """A binding-evaluation input with no real HTTP behind it."""
    return dict(
        status=200,
        body=b"{}",
        chain=chain,
        final_url=final_url or chain[-1],
        error=None,
        insecure_hop=insecure_hop,
        content_type="application/json",
    )


def json_fetch_result(url, doc):
    """A successful, non-redirected fetch of a given profile document."""
    return dict(
        status=200,
        body=json.dumps(doc).encode("utf-8"),
        chain=[url],
        final_url=url,
        error=None,
        insecure_hop=False,
        content_type="application/json",
    )


class FakeFetcher:
    """Serves canned fetch_result dicts by URL. No network calls."""

    def __init__(self, table):
        self.table = table

    def fetch(self, url):
        if url not in self.table:
            return dict(
                status=None, body=None, chain=[url], final_url=url,
                error=f"no fixture registered for {url}",
                insecure_hop=False, content_type=None,
            )
        return self.table[url]


# ---------------------------------------------------------- binding: Sec 11

def test_redirect_starting_over_http():
    """Sec 11.4: a chain that begins with HTTP must never bind, even if
    it lands on a conforming HTTPS document declaring the right host."""
    result = fetch_result(
        chain=["http://a.example/company.json", "https://cdn.example/profiles/a.json"],
        insecure_hop=True,  # the initial hop itself was insecure
    )
    binding, notes = resolver.evaluate_binding(result, "https://a.example/")
    check("HTTP-started redirect: binding is none", binding == "none", binding)
    check(
        "HTTP-started redirect: failure cites initial HTTPS",
        any("initial HTTPS" in n for n in notes),
        notes,
    )


def test_https_downgraded_mid_chain():
    """Sec 11.3 condition 5: the chain starts and ends on HTTPS, but a
    middle hop drops to HTTP. Distinct failure from Sec 11.4 above --
    the initial-HTTPS condition passes here; only the all-hops condition
    should fail."""
    result = fetch_result(
        chain=[
            "https://a.example/company.json",
            "http://mid.example/relay",
            "https://cdn.example/profiles/a.json",
        ],
        insecure_hop=True,  # the middle hop, not the first, was insecure
    )
    binding, notes = resolver.evaluate_binding(result, "https://a.example/")
    check("mid-chain downgrade: binding is none", binding == "none", binding)
    check(
        "mid-chain downgrade: failure cites all-hops-HTTPS",
        any("all hops HTTPS" in n for n in notes),
        notes,
    )
    check(
        "mid-chain downgrade: initial HTTPS is NOT among the failures "
        "(proves the two insecure-redirect cases are distinguished)",
        not any("initial HTTPS" in n for n in notes),
        notes,
    )


# --------------------------------------------------- reciprocity: Sec 9.10.2

def test_one_sided_relationship():
    """A declares brand -> B. B's profile exists, is fetchable, is
    first-party-bound, and simply never mentions A back. Valid profile
    data, but not mutual (spec Sec 9.10.2, 'Declared')."""
    b_profile = {"specVersion": "0.1", "name": "Org B", "url": "https://b.example/"}
    fetcher = FakeFetcher({
        "https://b.example/company.json": json_fetch_result(
            "https://b.example/company.json", b_profile
        ),
    })
    rel = {
        "type": "brand", "name": "Org B",
        "url": "https://b.example/", "profile": "https://b.example/company.json",
    }
    status, detail = resolver.evaluate_mutual(rel, "a.example", fetcher, None)
    check("one-sided relationship: status is declared", status == "declared", status)


def test_counterpart_unavailable():
    """The declared profile URL exists in the relationship, but the
    counterpart can't actually be retrieved -- connection failure or a
    plain 404. Either way: 'unavailable', not 'declared' or 'conflicting'."""
    rel = {
        "type": "brand", "name": "Org B",
        "url": "https://b.example/", "profile": "https://b.example/company.json",
    }

    conn_fail = FakeFetcher({
        "https://b.example/company.json": dict(
            status=None, body=None,
            chain=["https://b.example/company.json"],
            final_url="https://b.example/company.json",
            error="Connection refused", insecure_hop=False, content_type=None,
        ),
    })
    status, detail = resolver.evaluate_mutual(rel, "a.example", conn_fail, None)
    check("unavailable counterpart (connection failure): status is unavailable",
          status == "unavailable", status)
    check("unavailable counterpart (connection failure): detail cites the error",
          detail == "Connection refused", detail)

    not_found = FakeFetcher({
        "https://b.example/company.json": dict(
            status=404, body=None,
            chain=["https://b.example/company.json"],
            final_url="https://b.example/company.json",
            error=None, insecure_hop=False, content_type=None,
        ),
    })
    status, detail = resolver.evaluate_mutual(rel, "a.example", not_found, None)
    check("unavailable counterpart (404): status is unavailable",
          status == "unavailable", status)


def test_wrong_relationship_type():
    """A declares brand -> B (compatible reciprocal per spec Sec 9.10.1
    is parentOrganization). B declares a relationship back to A, but
    with an incompatible type. That is a conflict, not a match, and
    must not be reported as mutually-declared."""
    b_profile = {
        "specVersion": "0.1", "name": "Org B", "url": "https://b.example/",
        "relationships": [
            {"type": "affiliate", "name": "Org A", "url": "https://a.example/"},
        ],
    }
    fetcher = FakeFetcher({
        "https://b.example/company.json": json_fetch_result(
            "https://b.example/company.json", b_profile
        ),
    })
    rel = {
        "type": "brand", "name": "Org B",
        "url": "https://b.example/", "profile": "https://b.example/company.json",
    }
    status, detail = resolver.evaluate_mutual(rel, "a.example", fetcher, None)
    check("wrong relationship type: status is conflicting", status == "conflicting", status)


def test_relationship_profile_host_mismatch():
    """The relationship's own url and profile fields disagree about
    which host they name -- url points at Org B, profile points
    somewhere unrelated. Trusting profile here would let a relationship
    link one entity while proving reciprocity against a different one.
    Must refuse to evaluate rather than silently proceed."""
    rel = {
        "type": "brand", "name": "Org B",
        "url": "https://b.example/",
        "profile": "https://unrelated.example/company.json",
    }
    fetcher = FakeFetcher({})  # deliberately empty: must never be fetched
    status, detail = resolver.evaluate_mutual(rel, "a.example", fetcher, None)
    check("profile/url host mismatch: status is unavailable",
          status == "unavailable", status)
    check("profile/url host mismatch: detail explains the mismatch",
          "does not match" in detail, detail)


# ------------------------------------------------------------ host normalization

def test_normalize_host_preserves_nondefault_port():
    """Spec Sec 11.1 step 6: ignore only the *default* port for the
    scheme, not every port -- a non-default port must not be discarded,
    or example.com:8443 would wrongly bind as equivalent to example.com."""
    check("default HTTPS port (443) is ignored",
          resolver.normalize_host("https://example.com:443/x") == "example.com")
    check("default HTTP port (80) is ignored",
          resolver.normalize_host("http://example.com:80/x") == "example.com")
    check("non-default port is preserved",
          resolver.normalize_host("https://example.com:8443/x") == "example.com:8443")
    check("non-default port makes the host distinct from the bare host",
          resolver.normalize_host("https://example.com:8443/x")
          != resolver.normalize_host("https://example.com/x"))


# ----------------------------------------------------- version handling: Sec 12.1

SCHEMA_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..",
    "schema", "0.1", "company.schema.json",
)


def test_unsupported_specversion_not_treated_as_invalid():
    """Spec Sec 12.1: a document declaring an unsupported specVersion
    must be reported as unsupported, not silently run through the v0.1
    schema and reported as generically invalid."""
    doc = {"specVersion": "0.2", "name": "Org A", "url": "https://a.example/"}
    fetcher = FakeFetcher({
        "https://a.example/company.json": json_fetch_result(
            "https://a.example/company.json", doc
        ),
    })
    validator = (resolver.Draft202012Validator(json.load(open(SCHEMA_PATH)))
                 if resolver.Draft202012Validator else None)
    result = resolver.resolve("a.example", fetcher, validator, check_mutual=False)
    check("unsupported specVersion: recorded on the result",
          result.get("specVersion") == "0.2", result.get("specVersion"))
    check("unsupported specVersion: not run through the v0.1 validator "
          "(valid stays None, not False)",
          result["valid"] is None, result["valid"])
    check("unsupported specVersion: surfaced in notes",
          any("unsupported specVersion" in n for n in result["notes"]),
          result["notes"])


# ---------------------------------------------------------------------- main

def main():
    test_redirect_starting_over_http()
    test_https_downgraded_mid_chain()
    test_one_sided_relationship()
    test_counterpart_unavailable()
    test_wrong_relationship_type()
    test_relationship_profile_host_mismatch()
    test_normalize_host_preserves_nondefault_port()
    test_unsupported_specversion_not_treated_as_invalid()
    print(f"\n{'ALL TESTS PASS' if ok else 'FAILURES PRESENT'}")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
