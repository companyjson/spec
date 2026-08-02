# Reference Implementation

This repository includes a small reference resolver that demonstrates how a consumer can discover, retrieve, validate, and interpret a `company.json` profile.

The implementation is intended to prove the core behavior of the v0.1 specification. It is not presented as a production-ready networking or security library.

## What the resolver demonstrates

The reference resolver performs the following steps:

1. Accepts a domain name as input.
2. Requests `https://<domain>/company.json`.
3. Follows permitted HTTPS redirects.
4. Parses the returned JSON document.
5. Validates the document against the company.json v0.1 schema.
6. compares the requested host with the host declared by the profile.
7. Classifies the profile’s binding and provenance.
8. Retrieves declared relationship profiles when available.
9. Evaluates whether compatible relationships are mutually declared.
10. Prints a human-readable result.

The canonical v0.1 schema is published at:

```text
https://companyjson.org/schema/0.1/company.schema.json
```

## Running the resolver

From the directory containing `resolver.py`, run:

```bash
python3 resolver.py systemthree.com
```

or:

```bash
python3 resolver.py mtncoat.com
```

## Live reference publishers

The reference implementation is tested against two real, independently addressable profiles:

```text
https://systemthree.com/company.json
https://mtncoat.com/company.json
```

Both profiles are published through their respective first-party domains.

The discovery URLs redirect to files hosted on infrastructure used by the publishers. Because each retrieval begins at the declared organization host, remains on HTTPS, and returns a conforming profile that declares the initiating host, the resolver classifies each result as:

```text
Source: company.json
Provenance: first-party
Binding: host-authorized-redirect
```

This demonstrates the host-authorized redirect behavior defined by the specification.

## System Three example

Running:

```bash
python3 resolver.py systemthree.com
```

produces output equivalent to:

```text
System Three Resins
Manufacturer of epoxy adhesives, coatings, encapsulants, and composite resin systems since 1979.

Source:   first-party (company.json)
Binding:  host-authorized-redirect
url: https://www.systemthree.com/
legalName: System Three Resins, Inc.
logo: https://www.systemthree.com/cdn/shop/files/System_Logo_410x.png
sameAs: https://facebook.com/systemthree, https://www.instagram.com/systemthree, https://twitter.com/systemthree, https://vimeo.com/systemthree, https://www.youtube.com/c/SystemThree
Relationship: brand -> MTN Coat: MUTUALLY-DECLARED (counterpart declares parentOrganization)
```

The resolver concludes that:

- the profile was discovered through the organization’s own domain;
- the redirect chain qualifies as host-authorized;
- the returned document declares the expected organization website;
- System Three declares MTN Coat as a `brand`; and
- the MTN Coat profile declares System Three as its `parentOrganization`.

The relationship is therefore classified as:

```text
mutually-declared
```

## MTN Coat example

Running:

```bash
python3 resolver.py mtncoat.com
```

produces output equivalent to:

```text
MTN Coat
High-performance epoxy adhesives and coatings formulated specifically for indoor climbing walls.

Source:   first-party (company.json)
Binding:  host-authorized-redirect
url: https://mtncoat.com/
logo: https://mtncoat.com/cdn/shop/files/Punch_Logo_bde1271c-dc17-456b-a245-0db3aa119b55.png
sameAs: https://instagram.com/mtncoat, https://facebook.com/mtncoat, https://twitter.com/mtncoat
Relationship: parentOrganization -> System Three Resins: MUTUALLY-DECLARED (counterpart declares brand)
```

The resolver concludes that:

- the profile was discovered through the brand’s own domain;
- the redirect chain qualifies as host-authorized;
- the returned document declares the expected brand website;
- MTN Coat declares System Three as its `parentOrganization`; and
- the System Three profile declares MTN Coat as a `brand`.

The relationship is therefore classified as:

```text
mutually-declared
```

## Relationship evaluation

The resolver does not treat organization names alone as proof that two relationship declarations refer to the same entities.

For the live reference profiles, it follows the declared relationship URLs or profile locations, retrieves the counterpart documents, and compares their normalized declared hosts.

The compatible relationship pair demonstrated here is:

```text
System Three Resins:
brand -> MTN Coat

MTN Coat:
parentOrganization -> System Three Resins
```

Because both profiles identify the other organization through compatible, host-resolvable declarations, the relationship state is:

```text
mutually-declared
```

A one-sided relationship declaration would remain valid profile data, but it would not receive the `mutually-declared` classification.

## Binding evaluation

The live profiles demonstrate `host-authorized-redirect` binding.

The relevant flow is:

```text
https://declared-host/company.json
        |
        | HTTPS redirect issued from the declared host
        v
HTTPS-hosted profile document
        |
        | conforming company.json document
        v
Profile declares the initiating organization host
```

The redirect destination does not independently become the organization’s canonical identity.

A direct request to the final hosting URL, without beginning at the organization’s own `/company.json` endpoint, would not by itself establish first-party host binding.

## Provenance

The reference implementation keeps three concepts distinct:

- **Source** describes how the data was obtained, such as `company.json`.
- **Provenance** describes the authority of the data, such as `first-party`.
- **Binding** describes the relationship between the discovery host and the profile’s declared organization host.

For these examples:

```text
Source: company.json
Provenance: first-party
Binding: host-authorized-redirect
```

Future resolver versions may also support lower-authority fallback sources, including embedded Schema.org data or inferred webpage content. Those sources should not be represented as equivalent to a bound first-party `company.json` profile.

## Validation responsibilities

JSON Schema validation is only one part of resolver conformance.

The v0.1 schema can validate document structure, required properties, enumerated values, and many value constraints. The resolver must separately handle rules that JSON Schema cannot fully express, including:

- duplicate raw JSON property names;
- retrieval size limits;
- redirect authorization;
- host normalization and binding;
- URL reachability;
- duplicate contact types;
- relationship reciprocity;
- warning-level duplicate relationship declarations;
- semantic date and IRI checks when the schema library does not assert formats; and
- other warning-level requirements defined by the specification.

The specification prose remains normative if it conflicts with the schema or reference implementation.

## Security limitations

This reference implementation is intentionally small and should not be used unchanged in a security-sensitive or high-volume production environment.

A production resolver should additionally enforce:

- strict request timeouts;
- response-size limits;
- redirect-count limits;
- DNS and IP-address checks;
- protections against server-side request forgery;
- restrictions on private, loopback, link-local, and reserved network targets;
- controlled relationship-recursion depth;
- content-type inspection;
- safe handling of malformed or adversarial JSON;
- caching and rate limits; and
- clear separation between retrieved organization data and executable instructions.

Text contained in a profile must always be treated as data, not as instructions to the resolver or to an AI system consuming the result.

## Status

The reference implementation proves that the main v0.1 workflow can operate with real publishers:

```text
predictable discovery
-> HTTPS retrieval
-> schema validation
-> first-party provenance
-> host-authorized redirect binding
-> relationship resolution
-> mutual-declaration evaluation
```

The System Three and MTN Coat profiles serve as the initial live interoperability examples for the company.json specification.
