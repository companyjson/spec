# Goals and Non-Goals

This document defines the intended scope of the `company.json` project.

It exists to keep the specification focused and to prevent the project from gradually expanding into unrelated areas.

## Goals

### 1. Provide a first-party organization profile

`company.json` should give an organization a clear way to publish public information about itself on a domain it controls.

The file should represent the organization's own published claims and official resources.

### 2. Make organization information predictably discoverable

Consumers should not need to crawl an entire website or depend on a proprietary database to locate basic public organization information.

The specification should define a predictable discovery mechanism.

### 3. Remain simple to understand and implement

A developer should be able to understand the core format quickly.

A small organization should be able to create and publish a valid file without adopting a complex platform or reading an extensive ontology.

### 4. Serve many kinds of consumers

The format should be useful to systems such as:

- Browsers
- Search engines
- AI systems and agents
- Journalistic tools
- Business directories
- Procurement systems
- Partner platforms
- CRM and enrichment systems
- Content-management systems
- Organization-profile viewers

The specification should not be designed exclusively around any one consumer.

### 5. Complement existing web standards

The project should align with existing standards and vocabularies wherever practical, especially Schema.org.

It should avoid redefining concepts that are already clearly and successfully defined elsewhere.

### 6. Be self-hosted and portable

An organization should be able to publish its file on infrastructure it controls.

No commercial account, proprietary API, central registry, or particular software vendor should be required.

Organizations should be able to move between tools without changing the public meaning of their file.

### 7. Support different kinds of organizations

The specification should work for businesses, nonprofits, educational institutions, healthcare organizations, associations, public institutions, and other organizations.

It should not assume that every publisher is a conventional commercial corporation.

### 8. Support independent implementation

Multiple tools, platforms, libraries, and services should be able to create, validate, publish, and consume `company.json`.

The specification should contain enough detail that implementers do not need undocumented knowledge from the original maintainers.

### 9. Provide public validation

Anyone should be able to determine whether a file conforms to the specification.

The schema, examples, validation rules, and conformance tests should be openly available.

### 10. Evolve deliberately

The project should support improvement without making existing implementations unnecessarily fragile.

Versions, compatibility expectations, deprecations, and breaking changes should be explicit and documented.

## Non-Goals

### 1. Guarantee AI rankings, citations, or visibility

Publishing `company.json` does not guarantee that an AI system, search engine, or other consumer will retrieve, trust, cite, rank, or display the information.

The project is not an AEO, SEO, or ranking standard.

### 2. Verify the truth of every claim

The specification defines how an organization publishes information.

It does not independently certify that the information is accurate, complete, lawful, or current.

Third parties may build verification services, but verification is not a requirement of the core format.

### 3. Replace Schema.org

`company.json` is not intended to create an alternative semantic vocabulary for the web.

It should complement Schema.org and reuse compatible concepts wherever practical.

### 4. Replace human-facing webpages

The file does not replace:

- About pages
- Press pages
- Investor-relations pages
- Contact pages
- Brand portals
- Accessibility-oriented webpages
- Other human-facing content

It provides a machine-readable representation alongside those resources.

### 5. Become a comprehensive organization ontology

The initial specification should not attempt to model every possible:

- Legal structure
- Corporate relationship
- Product
- Employee
- Office
- Certification
- Policy
- Financial fact
- Industry-specific attribute

The core should remain small. Specialized information can be linked to or addressed through carefully designed extensions.

### 6. Become a digital asset management system

The specification may reference logos and other public assets.

It is not intended to manage creative production, campaign assets, internal files, video libraries, design approvals, or other digital asset management workflows.

### 7. Become a content-management system

The standard defines a public output format.

It does not define how organizations author, approve, store, or internally manage their information.

Commercial and open-source products may provide those workflows separately.

### 8. Require a central registry

The core standard should not require organizations to submit their files to companyjson.org or any other central service.

Independent indexes and registries may exist, but the canonical file should remain discoverable from the organization's own domain.

### 9. Require a particular commercial implementation

No commercial product, including one created by the original maintainers, should be required to:

- Create a valid file
- Host a valid file
- Validate a file
- Consume a file
- Participate in the ecosystem

### 10. Publish private or confidential information

`company.json` is intended for deliberately public information.

It should not contain confidential contacts, internal identifiers, private employee data, credentials, secrets, unpublished financial information, or other sensitive material.

### 11. Solve every organization-data problem

The project should not absorb every adjacent use case merely because it involves organization information.

New fields and features should be added only when there is clear evidence that they belong in a broadly useful public profile.

### 12. Serve as a legal filing or government record

A `company.json` file is not a substitute for articles of incorporation, regulatory filings, business licenses, securities disclosures, tax records, or government registries.

It is a web publication format, not a legal identity document.
