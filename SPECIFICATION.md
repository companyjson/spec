# company.json Specification

**Version:** 0.1 Draft
**Status:** Early implementation draft; not stable
**Last updated:** 2026-07-25

## Abstract

`company.json` is a plain-JSON format for publishing a canonical, first-party profile of an organization.

It provides a predictable way for software to retrieve basic organization information from a domain controlled by that organization or from a location explicitly authorized by that domain through a secure HTTP redirect.

The format is intended to complement existing standards such as Schema.org. It does not replace Schema.org, establish legal identity, independently verify claims, or create a central registry.

Version 0.1 intentionally defines a small core. Additional fields should be considered only after implementation experience with real publishers and consumers.

---

## 1. Purpose

Information about an organization is often distributed across websites, structured markup, social profiles, press pages, directories, databases, and third-party services.

Software attempting to answer basic questions may need to scrape webpages or reconcile conflicting sources:

* What is this organization called?
* What is its canonical website?
* How does it describe itself?
* Which logo is official?
* Which social profiles belong to it?
* How can it be contacted?
* Is it related to another organization or brand?

A `company.json` document allows an organization to publish answers to these questions in a simple, machine-readable form.

The primary design goals are:

1. **First-party publication**
   The organization publishes its profile on its own domain or explicitly delegates delivery through a secure redirect from its domain.

2. **Predictable structure**
   Consumers can retrieve known fields without interpreting arbitrary webpage layouts.

3. **Simple implementation**
   Publishers and consumers should not need specialized linked-data tooling.

4. **Compatibility with existing standards**
   Fields should map to Schema.org wherever an appropriate equivalent exists.

5. **Small, stable core**
   The specification should include only broadly useful organization information.

6. **Explicit provenance**
   Consumers should distinguish direct first-party publication, host-authorized delivery, embedded data, inferred data, and unrelated third-party declarations.

---

## 2. Scope

This specification defines:

* The structure of a `company.json` document
* Required and optional properties
* Validation and consumer-processing requirements
* Versioning behavior
* A provisional discovery convention
* Direct host binding and secure redirect-based host authorization
* A mechanism for namespaced extensions
* A pattern for mutually declared organization relationships

The format may be used by:

* Commercial businesses
* Nonprofit organizations
* Government entities
* Educational institutions
* Associations
* Brands with independent public identities
* Other organizations operating a public website

Although the project is named `company.json`, the format is not limited to incorporated companies.

---

## 3. Non-goals

`company.json` is not intended to:

* Independently verify that published claims are true
* Establish legal ownership or corporate authority
* Replace government or commercial registries
* Replace Schema.org
* Replace detailed brand-management standards
* Serve as a digital asset management system
* Publish product catalogs
* Describe software tools, agents, APIs, or MCP servers
* Rank organizations for search or AI visibility
* Guarantee consumption by search engines or AI systems
* Create a mandatory central directory
* Define a complete organization ontology
* Store sensitive, confidential, or nonpublic information

A conforming file is a first-party declaration only when it satisfies one of the binding methods defined in Section 11.

First-party publication provides provenance. It does not independently prove that every claim is accurate.

---

## 4. Requirement language

The key words **MUST**, **MUST NOT**, **REQUIRED**, **SHOULD**, **SHOULD NOT**, and **MAY** indicate requirement levels within this specification.

The prose of this specification is normative.

The published JSON Schema is a machine-readable conformance aid. If the schema and this specification conflict, this specification governs. Any divergence is a defect in the schema and should be reported.

Some requirements cannot be fully expressed in JSON Schema, including:

* Host-binding evaluation
* Redirect authorization
* URL reachability
* Duplicate property detection in raw JSON
* Reciprocal relationship checking
* Some SHOULD-level guidance
* Network and security behavior

Passing the JSON Schema therefore does not, by itself, demonstrate complete conformance with every requirement in this specification.

---

## 5. Conformance

### 5.1 Document conformance

A document conforms to a supported version of this specification when it:

1. Is valid JSON
2. Uses a top-level JSON object
3. Declares its specification version
4. Includes all properties required by that version
5. Follows the normative property rules for that version
6. Passes the JSON Schema published for that declared version
7. Contains no unknown core properties for that declared version

A document may be structurally conforming without qualifying as a first-party declaration.

### 5.2 Publisher conformance

A conforming publisher:

* Publishes a conforming document
* Serves it over HTTPS unless HTTPS is unavailable for a legitimate reason
* Publishes only information it is authorized to make public
* Does not describe an unrelated organization as though the document were that organization’s first-party profile
* Uses a discovery location supported by the applicable specification version
* Configures redirects deliberately when delegating profile delivery to another host

### 5.3 Consumer conformance

A conforming consumer:

* Determines the declared specification version before interpreting core properties
* Applies the schema and rules associated with the declared version when supported
* Performs binding evaluation before describing a profile as first-party, canonical, or authoritative
* Distinguishes direct host binding from host-authorized redirect delivery
* Ignores extension data it does not understand
* Handles unknown properties and enum values according to the forward-compatibility rules in this specification
* Does not treat publication as independent legal verification

### 5.4 Validator conformance

A conforming validator:

* Validates against the schema matching the declared specification version
* Does not validate a newer-version document as though it declared an older version
* Distinguishes unsupported versions from invalid documents
* Reports errors and warnings separately
* Identifies rules that require network, raw-input, or semantic checks beyond JSON Schema

---

## 6. Terminology

### Organization

The company, nonprofit, institution, association, brand, government body, or other entity described by the document.

### Publisher

The organization or authorized party that publishes the document.

### Consumer

Software that retrieves, validates, interprets, compares, or displays information from the document.

### Validator

Software that evaluates a document against this specification or its associated JSON Schema.

### Canonical website

The primary public website declared by the organization through the `url` property.

### Declared host

The normalized hostname of the canonical website declared in `url`.

### Discovery URL

A URL at which a consumer attempts to discover a profile according to this specification.

For version 0.1, the provisional discovery URL is:

```text
https://example.com/company.json
```

### Initial retrieval URL

The URL requested by the consumer before following redirects.

### Initial retrieval host

The normalized hostname of the initial retrieval URL.

### Final retrieval URL

The URL from which the profile document is ultimately returned after redirects.

### Final retrieval host

The normalized hostname of the final retrieval URL.

### Directly host-bound profile

A profile whose final retrieval host matches its declared host under the rules in Section 11.

### Host-authorized redirect

A secure HTTP redirect beginning at a recognized discovery URL on the declared host and explicitly directing the consumer to another HTTPS location from which the profile is returned.

### Redirect-authorized profile

A profile delivered from another host through a valid host-authorized redirect chain.

### First-party-bound profile

A profile that is either directly host-bound or redirect-authorized.

### First-party declaration

Information published through a first-party-bound profile.

### Profile

The organization information contained in a conforming `company.json` document.

### Specification version

The version of this specification against which the document was authored.

### Extension

A non-core property placed inside the `extensions` object and identified by a mechanically valid namespaced key.

### Declared relationship

A relationship stated by one organization’s profile.

### Mutually declared relationship

A compatible relationship stated by both organizations’ profiles.

---

## 7. Document format

A `company.json` document:

* MUST be valid JSON
* MUST use UTF-8 encoding
* MUST contain a JSON object at the top level
* MUST NOT contain duplicate property names
* MUST include `specVersion`, `name`, and `url`
* SHOULD be served with the media type `application/json`
* SHOULD be publicly retrievable without authentication
* SHOULD be delivered over HTTPS
* SHOULD permit standard HTTP caching
* SHOULD use absolute URLs
* MUST NOT include comments, trailing commas, or non-JSON syntax

The core format uses plain JSON. Publishers and consumers are not required to implement JSON-LD.

### 7.1 Recommended HTTP headers

A directly served profile SHOULD include:

```http
Content-Type: application/json; charset=utf-8
Access-Control-Allow-Origin: *
```

The `Access-Control-Allow-Origin: *` header allows public browser-based consumers, validators, and resolvers to retrieve the profile through cross-origin JavaScript requests without credentials.

When a profile is delivered through redirects:

* The response from the discovery URL SHOULD permit cross-origin retrieval.
* Each response in the redirect chain SHOULD be compatible with browser-based retrieval.
* The final profile response SHOULD include `Access-Control-Allow-Origin: *`.
* Publishers SHOULD test the complete redirect chain from a browser-based consumer.

The absence of a permissive CORS header does not make the JSON document structurally invalid. Consumers and validators MAY report it as a compatibility warning.

### 7.2 Document size

Consumers MUST support documents whose decoded body is no larger than **1 MiB**, equal to 1,048,576 bytes.

Consumers MAY support larger documents.

Consumers MAY reject documents larger than their supported limit, but MUST NOT reject a document solely for size when it is within the required 1 MiB minimum.

Publishers SHOULD keep profiles substantially smaller than this limit.

### 7.3 Duplicate property names

Duplicate property names are prohibited.

Because many JSON parsers silently discard all but one duplicated value, a validator that claims to enforce this rule MUST inspect the raw JSON input before or during parsing.

A validator operating only on an already-parsed object MUST disclose that it cannot reliably detect duplicate property names.

---

## 8. Core properties

| Property         |             Type | Required | Purpose                                                 |
| ---------------- | ---------------: | :------: | ------------------------------------------------------- |
| `specVersion`    |           string |    Yes   | Declares the specification version                      |
| `name`           |           string |    Yes   | Public name of the organization                         |
| `url`            |           string |    Yes   | Canonical website                                       |
| `legalName`      |           string |    No    | Registered legal name                                   |
| `alternateNames` | array of strings |    No    | Other recognized names                                  |
| `description`    |           string |    No    | Concise first-party description                         |
| `logo`           |           string |    No    | URL of the preferred official logo                      |
| `sameAs`         | array of strings |    No    | Official profiles hosted by other services              |
| `contacts`       | array of objects |    No    | Public contact channels                                 |
| `relationships`  | array of objects |    No    | Relationships to other organizations or brands          |
| `brandResources` |           string |    No    | URL of official brand or media resources                |
| `lastUpdated`    |           string |    No    | Date or date-time of the last meaningful profile update |
| `extensions`     |           object |    No    | Namespaced non-core data                                |

Properties not defined by the declared specification version MUST NOT appear at the top level of a conforming document.

Experimental or application-specific data MUST be placed inside `extensions`.

---

## 9. Property definitions

### 9.1 `specVersion`

The `specVersion` property declares the version of the `company.json` specification used by the document.

```json
{
  "specVersion": "0.1"
}
```

Requirements:

* MUST be a string
* MUST use the format `MAJOR.MINOR`
* For this draft, MUST equal `"0.1"`
* MUST describe the specification version, not the organization’s internal data revision

A validator encountering an unsupported declared version MUST report the document as using an unsupported specification version.

It MUST NOT report the document as invalid against a different version merely because that validator lacks support for the declared version.

---

### 9.2 `name`

The `name` property contains the primary public name of the organization.

```json
{
  "name": "Example Company"
}
```

Requirements:

* MUST be a non-empty string
* SHOULD use the name by which the organization publicly identifies itself
* SHOULD preserve the organization’s preferred capitalization and punctuation
* SHOULD NOT include slogans, promotional language, or descriptive suffixes that are not part of the public name

The public name may differ from the organization’s registered legal name.

Schema.org mapping: `schema:name`

---

### 9.3 `url`

The `url` property contains the canonical public website of the organization.

```json
{
  "url": "https://example.com/"
}
```

Requirements:

* MUST be an absolute HTTP or HTTPS URL
* SHOULD use HTTPS
* SHOULD identify the primary website of the organization
* SHOULD use the preferred canonical hostname
* SHOULD resolve successfully
* SHOULD use a trailing slash when referring to the website root
* MUST NOT contain embedded credentials
* MUST NOT use a fragment to identify the organization

The host in `url` is used in the binding evaluation defined in Section 11.

Schema.org mapping: `schema:url`

---

### 9.4 `legalName`

The `legalName` property contains the organization’s registered or formal legal name.

```json
{
  "legalName": "Example Company Holdings, Inc."
}
```

Requirements:

* MUST be a non-empty string when present
* SHOULD be omitted when the publisher cannot confidently identify the applicable legal entity
* MUST NOT be interpreted as legal verification by the `company.json` project or by a consumer

Schema.org mapping: `schema:legalName`

---

### 9.5 `alternateNames`

The `alternateNames` property contains other names by which the organization is commonly or historically known.

```json
{
  "alternateNames": [
    "Example Co.",
    "Example Holdings"
  ]
}
```

Requirements:

* MUST be an array of non-empty strings
* MUST NOT include duplicate values
* SHOULD NOT repeat the value of `name`
* MAY include abbreviations, former names, trading names, or common variations
* SHOULD NOT include keywords or promotional phrases merely intended to improve discoverability

Schema.org mapping: `schema:alternateName`

---

### 9.6 `description`

The `description` property contains a concise first-party description of the organization.

```json
{
  "description": "A manufacturer of specialty adhesives and protective coatings."
}
```

Requirements:

* MUST be a non-empty string when present
* SHOULD describe what the organization is or does
* SHOULD be understandable without additional webpage context
* SHOULD avoid temporary promotional language
* SHOULD generally remain concise enough for reuse by software consumers
* MUST NOT contain HTML markup

Schema.org mapping: `schema:description`

---

### 9.7 `logo`

The `logo` property contains the URL of the organization’s preferred official logo.

```json
{
  "logo": "https://example.com/assets/logo.svg"
}
```

Requirements:

* MUST be an absolute HTTP or HTTPS URL
* SHOULD use HTTPS
* SHOULD resolve directly to an image resource
* SHOULD identify a current, approved logo
* SHOULD use a durable URL
* SHOULD use SVG, PNG, WebP, or another broadly supported web image format
* SHOULD NOT identify a temporary campaign image
* SHOULD NOT identify a webpage that merely contains the logo

Version 0.1 permits one preferred logo in the core profile.

Alternative formats, colorways, usage restrictions, and complete brand systems belong in `brandResources`, an external brand profile, or a namespaced extension.

Schema.org mapping: `schema:logo`

---

### 9.8 `sameAs`

The `sameAs` property contains official organization profiles hosted by other services.

```json
{
  "sameAs": [
    "https://www.linkedin.com/company/example",
    "https://github.com/example"
  ]
}
```

Requirements:

* MUST be an array of absolute HTTP or HTTPS URLs
* MUST NOT contain duplicate values
* SHOULD include only profiles that represent the organization itself
* SHOULD NOT include ordinary mentions, distributor pages, customer pages, or unrelated directory listings
* SHOULD use canonical profile URLs when known

Examples may include:

* Official social profiles
* Official developer-organization profiles
* Authoritative knowledge-base entries
* Government or institutional directory pages represented by URLs

Non-URL legal, financial, registry, or commercial identifiers are outside the scope of `sameAs` in version 0.1.

Schema.org mapping: `schema:sameAs`

---

### 9.9 `contacts`

The `contacts` property contains public contact channels for defined purposes.

```json
{
  "contacts": [
    {
      "type": "general",
      "email": "hello@example.com",
      "url": "https://example.com/contact"
    },
    {
      "type": "press",
      "email": "press@example.com"
    }
  ]
}
```

Each contact object:

* MUST include `type`
* MUST include at least one of `email`, `telephone`, or `url`
* MAY include `name`
* MUST contain only public contact information intended for the declared purpose

Supported properties:

| Property    |   Type |   Required  | Purpose                                  |
| ----------- | -----: | :---------: | ---------------------------------------- |
| `type`      | string |     Yes     | Purpose of the contact                   |
| `name`      | string | Conditional | Public name of the team or contact point |
| `email`     | string |      No     | Public email address                     |
| `telephone` | string |      No     | Public telephone number                  |
| `url`       | string |      No     | Public contact or support page           |

Initial contact types are:

* `general`
* `press`
* `support`
* `sales`
* `security`
* `privacy`
* `other`

Requirements:

* The array MUST NOT contain more than one contact object with the same `type`
* A contact with `"type": "other"` MUST include a non-empty `name`
* `email` SHOULD contain a plain email address rather than a `mailto:` URL
* `telephone` SHOULD use an internationally understandable format
* `url` MUST be an absolute HTTP or HTTPS URL
* Personal contact information SHOULD NOT be included unless intentionally published for that purpose

Consumers processing a supported specification version but encountering an unsupported future `type` value MUST ignore that contact entry rather than reject the entire profile.

Schema.org mapping: `schema:contactPoint`

---

### 9.10 `relationships`

The `relationships` property describes selected public relationships between the organization and another organization or brand.

```json
{
  "relationships": [
    {
      "type": "parentOrganization",
      "name": "Example Holdings",
      "url": "https://exampleholdings.com/",
      "profile": "https://exampleholdings.com/company.json"
    }
  ]
}
```

Each relationship object:

* MUST include `type`
* MUST include `name`
* SHOULD include `url`
* MAY include `profile`

Supported properties:

| Property  |   Type | Required | Purpose                                                 |
| --------- | -----: | :------: | ------------------------------------------------------- |
| `type`    | string |    Yes   | Nature of the relationship                              |
| `name`    | string |    Yes   | Public name of the related entity                       |
| `url`     | string |    No    | Canonical website of the related entity                 |
| `profile` | string |    No    | Direct or discovery URL of the related entity’s profile |

Initial relationship types are:

* `parentOrganization`
* `subOrganization`
* `brand`
* `member`
* `memberOf`
* `affiliate`

Requirements:

* Relationships MUST be intentionally declared by the publisher
* `url`, when present, MUST be an absolute HTTP or HTTPS URL
* `profile`, when present, MUST be an absolute HTTP or HTTPS URL
* The presence of a relationship in one profile does not guarantee a reciprocal declaration
* Relationship declarations MUST NOT be treated as legal proof of ownership, control, affiliation, or membership
* Duplicate relationship objects do not invalidate the profile, but SHOULD be reported by validators
* Consumers MAY collapse structurally identical duplicate relationship objects
* Consumers MUST NOT assign additional weight or meaning to a relationship because it appears more than once

Consumers processing a supported specification version but encountering an unsupported future `type` value MUST ignore that relationship entry rather than reject the entire profile.

Schema.org mappings may include:

* `schema:parentOrganization`
* `schema:subOrganization`
* `schema:brand`
* `schema:member`
* `schema:memberOf`

Some relationships may not map perfectly and will be documented separately.

#### 9.10.1 Compatible reciprocal relationship types

The following relationship types are compatible reciprocals in version 0.1:

| One profile declares | Counterpart declares         |
| -------------------- | ---------------------------- |
| `parentOrganization` | `subOrganization` or `brand` |
| `subOrganization`    | `parentOrganization`         |
| `brand`              | `parentOrganization`         |
| `memberOf`           | `member`                     |
| `member`             | `memberOf`                   |
| `affiliate`          | `affiliate`                  |

#### 9.10.2 Mutual declaration evaluation

A relationship is **declared** when it appears in one organization’s profile.

A relationship may be classified as **mutually declared** when all of the following are true:

1. The original relationship includes a `profile` URL.
2. The referenced profile is successfully retrieved.
3. The referenced profile is structurally valid.
4. The referenced profile is first-party-bound under Section 11.
5. The referenced profile contains a compatible reciprocal relationship type.
6. The reciprocal relationship mechanically identifies the original organization.

A reciprocal relationship mechanically identifies the original organization when at least one of the following is true:

* The normalized host of the reciprocal relationship’s `url` equals the declared host of the original profile.
* The normalized host of the reciprocal relationship’s `profile` equals the declared host of the original profile.
* Retrieval of the reciprocal relationship’s `profile` produces a valid first-party-bound profile whose declared host equals the declared host of the original profile.

All host comparisons MUST use the normalization rules in Section 11.1.

Name matching alone MUST NOT establish reciprocity.

Consumers MAY fetch referenced profiles to evaluate reciprocity.

Consumers that perform this check SHOULD distinguish among:

* **Declared:** stated only by the current profile
* **Mutually declared:** compatible declarations appear in both profiles
* **Conflicting:** the counterpart profile makes an incompatible declaration
* **Not evaluated:** the consumer did not retrieve or compare the counterpart
* **Unavailable:** the counterpart profile could not be retrieved or validated

A mutually declared relationship provides stronger first-party provenance than a unilateral declaration. It does not independently establish legal ownership, control, affiliation, or membership.

---

### 9.11 `brandResources`

The `brandResources` property contains the URL of an official brand, press, or media-resource page.

```json
{
  "brandResources": "https://example.com/brand"
}
```

Requirements:

* MUST be an absolute HTTP or HTTPS URL
* SHOULD use HTTPS
* SHOULD identify a resource maintained or approved by the organization
* MAY link to a webpage, downloadable media kit, digital asset system, or supported external brand profile

Detailed information such as color palettes, typography, advertising instructions, usage restrictions, and complete logo collections is outside the core scope of `company.json`.

No exact Schema.org mapping is defined in version 0.1.

---

### 9.12 `lastUpdated`

The `lastUpdated` property identifies when the profile was last meaningfully reviewed or changed.

```json
{
  "lastUpdated": "2026-07-25"
}
```

It MUST contain either:

* An RFC 3339 `full-date`, such as `2026-07-25`; or
* An RFC 3339 `date-time`, such as `2026-07-25T18:30:00Z`

Requirements:

* MUST conform to one of the two formats above
* SHOULD represent a meaningful review or profile update
* SHOULD NOT change solely because the file was rebuilt without substantive changes
* MUST NOT be interpreted as proof that every individual field was independently verified on that date

Possible Schema.org mapping: `schema:dateModified`

---

### 9.13 `extensions`

The `extensions` property allows experimental or application-specific information without expanding the core specification.

```json
{
  "extensions": {
    "com.example.certifications": {
      "status": "active"
    }
  }
}
```

Requirements:

* MUST be a JSON object
* Each extension key MUST satisfy one of the two key formats defined below
* Extension values MAY contain any valid JSON value
* Extensions MUST NOT alter the meaning of core properties
* Consumers MUST ignore extensions they do not understand
* Publishers MUST NOT require consumers to process an extension in order to interpret the core profile

An extension key MUST be either:

1. An absolute URI; or
2. A reverse-domain-style name containing at least two non-empty dot-separated labels

For reverse-domain-style keys:

* Each label MUST contain only ASCII letters, digits, or hyphens
* A label MUST NOT begin or end with a hyphen
* The complete key MUST contain at least one period
* Keys are case-sensitive, but lowercase is strongly recommended

Examples of acceptable extension keys:

```text
com.example.certifications
org.companyjson.experimental.locations
https://example.com/vocab/disclosures
```

Examples of unacceptable extension keys:

```text
certifications
custom
extraData
.example
example.
com..example
```

Use of an extension does not imply endorsement by the `company.json` project.

---

## 10. Provisional discovery

Discovery is intentionally provisional in version 0.1.

For implementation testing, publishers MAY make the document available at:

```text
https://example.com/company.json
```

Consumers MAY attempt to retrieve `/company.json` from an organization’s canonical hostname.

Consumers MAY also accept a direct profile URL supplied through:

* User input
* Configuration
* An API response
* A webpage link
* Another trusted discovery mechanism

However:

* `/company.json` is not yet a permanently standardized discovery location
* Consumers MUST NOT automatically probe an unregistered `/.well-known/` suffix for this format
* A future version may define a registered `/.well-known/` location
* A future version may define discovery through HTTP headers, HTML links, DNS, or another mechanism
* Publishers SHOULD NOT assume that the provisional root location will remain unchanged in a future major version
* Implementations SHOULD make the discovery location configurable during the draft period

The project will evaluate existing conventions, including the registered `openorg` well-known URI, before proposing a permanent discovery mechanism.

### 10.1 Redirects

Consumers MAY follow HTTP redirects while retrieving a profile.

Consumers SHOULD:

* Apply a finite redirect limit
* Protect against redirect loops
* Record the complete redirect chain
* Record the initial and final retrieval URLs
* Avoid following redirects to unsupported URL schemes
* Refuse HTTPS-to-HTTP downgrades
* Apply response-size and request-time limits
* Perform binding evaluation after retrieval

A redirect to another host does not automatically disqualify a profile from first-party treatment. It may qualify as a host-authorized redirect under Section 11.3.

Redirect authorization requires the initial request and every redirect target to use HTTPS.

---

## 11. Authority and binding

A profile qualifies as a first-party declaration only when it is either:

1. Directly host-bound; or
2. Redirect-authorized.

Consumers MUST determine and expose the applicable binding result.

Recommended binding result labels are:

```text
direct
host-authorized-redirect
none
```

### 11.1 Host normalization

Before comparing hostnames, consumers MUST:

1. Parse the value as an HTTP or HTTPS URL.
2. Convert the domain to its ASCII form using domain-to-ASCII processing.
3. Convert ASCII letters to lowercase.
4. Remove a trailing DNS root period, when present.
5. Remove exactly one leading `www.` label for comparison purposes.
6. Ignore the default port for the URL scheme.

Examples treated as equivalent:

```text
example.com
www.example.com
EXAMPLE.COM
example.com.
```

The following are not automatically equivalent:

```text
assets.example.com
shop.example.com
example.net
example.github.io
```

Consumers MUST NOT treat arbitrary subdomains, sibling domains, or domains sharing the same registrable domain as equivalent solely for binding.

### 11.2 Direct host binding

A profile is directly host-bound when the normalized final retrieval host equals the normalized declared host.

Examples:

| Final retrieval URL                       | Declared `url`             | Result                  |
| ----------------------------------------- | -------------------------- | ----------------------- |
| `https://example.com/company.json`        | `https://example.com/`     | Directly host-bound     |
| `https://www.example.com/company.json`    | `https://example.com/`     | Directly host-bound     |
| `https://example.com/company.json`        | `https://www.example.com/` | Directly host-bound     |
| `https://assets.example.com/company.json` | `https://example.com/`     | Not directly host-bound |
| `https://evil.example/company.json`       | `https://example.com/`     | Not directly host-bound |

A direct profile URL does not need to use `/company.json` to qualify for direct host binding, provided the final retrieval host matches the declared host.

A directly host-bound profile retrieved over plain HTTP may qualify as directly bound, but consumers SHOULD report the absence of HTTPS as a security warning.

### 11.3 Host-authorized redirect binding

A profile may qualify as redirect-authorized when it is delivered from another host through a secure redirect originating at the organization’s recognized discovery URL.

For version 0.1, redirect authorization requires all of the following:

1. The initial retrieval URL uses HTTPS.
2. The initial retrieval URL uses the provisional discovery path `/company.json`.
3. The normalized initial retrieval host equals the normalized declared host.
4. The response from the initial host explicitly redirects the consumer to another HTTPS URL.
5. Every URL in the redirect chain uses HTTPS.
6. The final response contains a structurally conforming profile.
7. The profile’s declared host matches the normalized initial retrieval host.
8. The redirect chain remains within the consumer’s configured redirect, time, and size limits.

Example:

```text
https://example.com/company.json
        ↓ 302
https://cdn.example-provider.com/profiles/example-company.json
        ↓ 200
company.json document
```

If the document declares:

```json
{
  "url": "https://example.com/"
}
```

the profile may be classified as:

```text
host-authorized-redirect
```

The secure redirect issued from the declared host acts as an explicit authorization to retrieve the profile from the destination location.

### 11.4 Limits of redirect authorization

A redirect chain beginning with an HTTP request MUST NOT establish redirect authorization, even if the returned document is otherwise conforming.

A consumer MAY still process such a document, but its redirect-based binding result MUST be:

```text
none
```

A direct request to a third-party or CDN URL does not qualify as first-party solely because the returned document declares another organization’s domain.

For example, requesting this URL directly:

```text
https://cdn.example-provider.com/profiles/example-company.json
```

does not establish first-party provenance for `example.com`.

The consumer must have begun at:

```text
https://example.com/company.json
```

and followed the secure redirect issued by that host.

A consumer evaluating redirect authorization MUST record:

* Initial retrieval URL
* Initial retrieval host
* Redirect chain
* Final retrieval URL
* Final retrieval host
* Declared host
* Binding result

Consumers SHOULD expose redirect-authorized profiles as:

```text
First-party via host-authorized redirect
```

rather than presenting them as directly hosted.

### 11.5 Treatment of profiles without binding

When a profile is neither directly host-bound nor redirect-authorized:

* A consumer MUST NOT label it first-party
* A consumer MUST NOT label it canonical
* A consumer MUST NOT label it authoritative for the declared website
* A consumer MUST surface or record the mismatch
* A consumer MAY display the data as an unverified third-party declaration
* A consumer MAY continue processing the document for diagnostic or comparison purposes

A failed binding result does not necessarily mean the document is malicious. It may result from:

* Incorrect configuration
* A stale canonical URL
* An unsupported hosting arrangement
* A directly supplied CDN URL
* An insecure redirect chain
* An unauthorized or deceptive publication

### 11.6 Scope of authority

A first-party-bound profile is authoritative only as a declaration published or authorized by the website identified in `url`.

It does not prove:

* Ownership of other domains
* Ownership of referenced brands
* Legal control of related organizations
* Accuracy of registry information
* Trustworthiness of the organization
* Continued accuracy after publication
* That the domain itself has not been compromised

---

## 12. Validation and processing rules

### 12.1 Version-specific validation

Validators MUST use the schema corresponding to the document’s declared `specVersion`.

A document declaring version `0.1`:

* MUST contain only core properties defined in version 0.1
* MUST satisfy the version 0.1 schema
* MUST place experimental data under `extensions`

A document declaring an unsupported version:

* MUST be reported as using an unsupported version
* MUST NOT be treated as malformed solely because the validator lacks the matching schema
* MAY be processed partially under the forward-compatibility rules below

### 12.2 Strict schemas and tolerant consumers

Schemas are strict within a declared specification version.

Consumers are tolerant across compatible minor versions.

A consumer that supports version 0.1 and elects to process a document declaring a later minor version, such as 0.2:

* MUST NOT silently treat the document as version 0.1
* MUST identify that full validation was not performed
* MUST ignore unknown top-level properties
* MUST ignore unknown properties inside recognized core objects
* MUST ignore individual contact or relationship entries with unsupported enum values
* MAY process recognized properties whose meaning remains compatible
* MUST NOT describe the newer-version document as fully validated against version 0.1

A consumer MAY instead decline to process an unsupported version.

### 12.3 Strict validation mode

A validator MAY offer a strict or lint mode intended for:

* Continuous integration
* Reference implementations
* Specification development
* Publisher quality control

Strict mode may elevate warnings to errors, including:

* Missing HTTPS
* Missing CORS headers
* URL reachability failures
* Missing recommended fields
* Noncanonical formatting
* Failed binding
* Duplicate objects
* Unrecognized values encountered during compatibility processing

Strict mode does not change the normative structural-validity rules of the declared specification version.

### 12.4 String validation

Unless otherwise specified:

* Required strings MUST contain at least one non-whitespace character
* Leading and trailing whitespace SHOULD be reported
* Human-readable values MUST NOT contain HTML markup
* Strings SHOULD preserve intended Unicode characters

### 12.5 URL validation

Unless otherwise specified:

* URLs MUST be absolute
* URLs MUST use HTTP or HTTPS
* Production URLs SHOULD use HTTPS
* URLs MUST NOT contain embedded credentials
* Consumers SHOULD handle redirects safely
* Validators MAY warn when a URL is unreachable
* Network failure MUST be distinguished from structural invalidity

A syntactically valid URL is not guaranteed to be active, safe, authoritative, or controlled by the publisher.

### 12.6 Array validation

Unless a property-specific rule states otherwise:

* Arrays MUST NOT contain duplicate primitive values.
* Duplicate objects do not invalidate the document, but validators SHOULD report them.
* Consumers MAY collapse byte-identical or structurally identical duplicate objects.
* Consumers MUST NOT assign additional weight or meaning to repeated objects.
* Empty arrays SHOULD be omitted.
* Array order MUST NOT carry semantic meaning.

Property-specific uniqueness requirements take precedence over these general rules.

For example:

* `alternateNames` MUST NOT contain duplicate string values.
* `sameAs` MUST NOT contain duplicate URL values.
* `contacts` MUST NOT contain more than one object with the same `type`, even when the objects are not identical.
* Duplicate relationship objects are valid but SHOULD produce a warning.

### 12.7 Unknown data

For a document declaring a supported version:

* Unknown top-level properties are invalid
* Unknown properties inside defined core objects are invalid
* Experimental data MUST appear under `extensions`

For compatibility processing of a later unsupported minor version:

* Unknown properties are ignored
* Unsupported enum entries are ignored at the entry level
* Recognized compatible properties may still be processed

Unknown extensions MUST always be ignored by consumers.

### 12.8 Error reporting

Validators SHOULD:

* Identify the property or JSON location that failed
* Explain the expected type or rule
* Distinguish errors from warnings
* Distinguish unsupported versions from invalid documents
* Distinguish structural validation from binding evaluation
* Distinguish direct binding from redirect authorization
* Report missing CORS headers as compatibility warnings
* Report duplicate relationship objects as warnings
* Report insecure redirect chains as binding failures
* Provide actionable remediation
* Avoid exposing stack traces or implementation-specific errors to ordinary users

---

## 13. Versioning

The specification uses major and minor versions:

```text
MAJOR.MINOR
```

Examples:

```text
0.1
0.2
1.0
```

### 13.1 Draft versions

Versions beginning with `0.` are drafts.

During the draft period:

* Properties may be added, changed, or removed
* Discovery behavior may change
* Publishers should expect migration
* Consumers must inspect `specVersion`
* Breaking changes must be documented clearly

Compatibility between draft minor versions is a design goal but is not guaranteed until version 1.0.

### 13.2 Minor versions

A minor version may:

* Add optional properties
* Add allowed enum values
* Clarify validation behavior
* Add mappings or examples
* Make backward-compatible corrections

A minor version MUST NOT intentionally change the meaning of an existing property in an incompatible way.

Older consumers may process recognized data from newer minor versions according to Section 12.2.

### 13.3 Major versions

A major version is required when a change:

* Removes or renames a property
* Changes the meaning of an existing property incompatibly
* Makes an optional property required
* Changes the document structure incompatibly
* Changes discovery in a way that breaks existing implementations
* Changes binding semantics incompatibly

### 13.4 Version declaration

Every document MUST declare its specification version through `specVersion`.

Version 0.1 does not define a separate document-revision property. HTTP metadata, source control, and `lastUpdated` may be used to track profile changes.

---

## 14. Schema.org relationship

`company.json` uses a constrained plain-JSON structure.

The project will maintain a formal mapping between core properties and Schema.org wherever a suitable equivalent exists.

The mapping is intended to:

* Avoid inventing unnecessary competing terminology
* Support conversion to Schema.org JSON-LD
* Help consumers reconcile `company.json` with webpage structured data
* Identify cases where meanings differ or no direct equivalent exists

A `company.json` document is not itself JSON-LD and does not require an `@context`.

Conformance to this specification does not imply conformance to Schema.org, and Schema.org markup does not imply conformance to this specification.

The normative meaning of a `company.json` property is defined by this specification. Schema.org mappings are interoperability guidance unless explicitly incorporated into a future normative version.

---

## 15. Security and privacy considerations

Publishers should assume that every value in a `company.json` document is public and may be:

* Indexed
* Cached
* Republished
* Archived
* Compared with other sources
* Used by automated systems

Publishers MUST NOT include:

* Passwords
* API keys
* Authentication tokens
* Private employee information
* Nonpublic email addresses
* Confidential identifiers
* Internal system locations
* Information the organization is not authorized to publish

Consumers MUST treat all values as untrusted input.

Consumers displaying or processing profile data SHOULD:

* Escape output appropriately
* Avoid executing embedded content
* Validate URLs before making requests
* Protect against server-side request forgery
* Apply request timeouts
* Apply response-size limits
* Limit redirect depth
* Reject unsupported URL schemes
* Refuse HTTPS-to-HTTP downgrades
* Avoid automatically downloading large or executable resources
* Protect against recursive relationship fetching
* Cache responsibly
* Avoid treating profile text as trusted instructions

Consumers evaluating mutual relationships SHOULD limit:

* Fetch depth
* Total fetched profiles
* Request duration
* Repeated circular references

Redirect authorization relies on the integrity of the redirect response issued by the declared host.

An initial HTTP request can be modified by an on-path attacker. An attacker capable of modifying that response could inject a redirect to an attacker-controlled profile and falsely appear to delegate first-party authority.

For this reason:

* Redirect-authorized retrieval MUST begin with HTTPS.
* Every URL in the redirect chain MUST use HTTPS.
* A redirect chain beginning with HTTP MUST NOT establish redirect authorization.

Direct host binding may still be evaluated for a document retrieved over HTTP, but consumers SHOULD clearly report the insecure transport.

Redirect authorization indicates that the declared host securely directed the consumer to the final profile location. It does not prove that:

* The destination host is permanently controlled by the organization
* The destination has not been compromised
* Every claim in the profile is legally accurate
* The profile is current
* Every referenced relationship is valid
* The organization is trustworthy

Verification and trust scoring are outside the scope of this specification.

---

## 16. Minimal example

```json
{
  "specVersion": "0.1",
  "name": "Example Company",
  "url": "https://example.com/"
}
```

This is the smallest conforming version 0.1 document.

It is first-party only when it is directly host-bound or redirect-authorized under Section 11.

---

## 17. Extended example

```json
{
  "specVersion": "0.1",
  "name": "Example Company",
  "legalName": "Example Company Holdings, Inc.",
  "alternateNames": [
    "Example Co."
  ],
  "url": "https://example.com/",
  "description": "A manufacturer of specialty adhesives and protective coatings.",
  "logo": "https://example.com/assets/logo.svg",
  "sameAs": [
    "https://www.linkedin.com/company/example",
    "https://github.com/example"
  ],
  "contacts": [
    {
      "type": "general",
      "email": "hello@example.com",
      "url": "https://example.com/contact"
    },
    {
      "type": "press",
      "email": "press@example.com"
    }
  ],
  "relationships": [
    {
      "type": "brand",
      "name": "Example Industrial",
      "url": "https://industrial.example.com/",
      "profile": "https://industrial.example.com/company.json"
    }
  ],
  "brandResources": "https://example.com/brand",
  "lastUpdated": "2026-07-25"
}
```

---

## 18. Open questions for version 0.1

The following questions remain intentionally unresolved:

1. What should the permanent discovery mechanism be?
2. How should this specification relate operationally to `openorg`?
3. Should a future version support explicit delegation without an HTTP redirect?
4. Should a profile identify additional domains it is authorized to describe?
5. Should the core include structured postal addresses?
6. Should the core include legal, financial, or registry identifiers?
7. Are the initial relationship types sufficient and unambiguous?
8. Should logos eventually support multiple formats or variants?
9. Should multilingual values be supported in the core?
10. Should `lastUpdated` become required?
11. Which properties have sufficiently exact Schema.org mappings?
12. Should an HTTP response header or HTML link advertise the profile?
13. Should later versions permit multiple contacts of the same type with language, region, or department qualifiers?
14. Is 1 MiB the appropriate long-term minimum consumer limit?
15. Should a future version define cryptographic signing or content-digest guidance?
16. Should redirect authorization eventually require additional integrity or caching guidance?
17. Should CORS support become mandatory after implementation experience?

These questions should be resolved through implementation experience and feedback from publishers and consumers.

---

## 19. Change policy

Version 0.1 is an implementation draft.

Changes should be guided by:

* Experience from live reference implementations
* Independent publisher feedback
* Independent consumer feedback
* Compatibility with existing web standards
* Evidence that a field is broadly useful
* The goal of keeping the core small

A proposed field should not be added merely because some organization could publish it.

It should be added only when:

1. Multiple publishers are likely to maintain it,
2. Multiple consumers can use it,
3. Its meaning can be defined clearly,
4. It does not belong more naturally in an existing complementary standard, and
5. It can be implemented without disproportionate complexity.
