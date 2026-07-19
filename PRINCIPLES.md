# Principles

These principles guide the design, governance, and evolution of the `company.json` specification.

When individual feature requests conflict with these principles, the principles should take priority.

## 1. Obviousness over cleverness

The specification should feel predictable.

Names, fields, examples, and discovery mechanisms should be understandable without unnecessary terminology or branding.

A developer should be able to correctly anticipate much of the format before reading the full specification.

## 2. The smallest useful core

The core specification should contain only information that is broadly useful across many kinds of organizations and consumers.

Every additional field creates implementation, documentation, validation, privacy, and compatibility costs.

When uncertain, leave a field out until real implementations demonstrate that it belongs.

## 3. First-party and domain-controlled

The canonical file should be published on a domain controlled by the organization it describes.

The organization—not a platform, registry, directory, or software vendor—should control its public profile.

## 4. Publication is not certification

A valid `company.json` file represents claims published by the organization.

Validation confirms that the file follows the specification. It does not independently prove that the claims are accurate or trustworthy.

Consumers remain responsible for applying their own verification and trust policies.

## 5. Complement existing standards

The project should reuse and align with successful web standards and vocabularies wherever practical.

In particular, it should complement Schema.org rather than create a competing definition of an organization.

New concepts should be invented only when existing standards do not adequately address the requirement.

## 6. Open and vendor-neutral

The specification, schema, examples, and validation rules should be publicly available.

No proprietary account, API, identifier, registry, or commercial service should be required to create, host, validate, or consume a valid file.

No commercial implementation should receive privileged treatment in the specification.

## 7. Self-hosted and portable

Organizations should be able to publish `company.json` using ordinary web infrastructure.

The format should remain useful if any particular software vendor, hosting provider, registry, or maintainer disappears.

An organization should be able to change management tools without changing the public meaning of its file.

## 8. Human-reviewable and machine-reliable

The file is designed for machines, but people should be able to inspect and understand it.

The format should avoid unnecessary abstraction, opaque identifiers, and structures that are difficult for an organization to review.

At the same time, field definitions should be precise enough that independent software interprets them consistently.

## 9. Public by design

`company.json` is intended for information an organization deliberately publishes to the open web.

The specification should avoid encouraging the publication of confidential, sensitive, internal, or unnecessary personal information.

Fields should be evaluated not only for usefulness but also for privacy and abuse risks.

## 10. Independent implementation

A developer should be able to implement the specification using only the public documentation, schema, examples, and conformance tests.

Undocumented behavior, vendor-specific assumptions, or dependence on the original maintainers should be treated as defects.

## 11. Stable and explicit evolution

Before version 1.0, the project may make breaking changes as implementation experience reveals better designs.

Those changes should still be documented clearly.

After version 1.0, backward compatibility should be the default. Breaking changes should be rare, intentional, versioned, and accompanied by migration guidance.

Published versions must never change meaning silently.

## 12. Extensibility without fragmentation

The core should remain small, but the specification should not prevent experimentation or specialized use cases.

Extensions should be optional, clearly identified, and designed so that consumers can safely ignore what they do not understand.

Vendor-specific experimentation must not turn the core format into an unstructured collection of proprietary fields.

Extensions should enter the core only after broad usefulness has been demonstrated.

## 13. Evidence over speculation

Changes should be driven by real implementation and consumption experience.

A field should not be added merely because it might someday be useful.

Priority should be given to documented needs from publishers, consumers, and independent implementers.

## 14. The standard and commercial tooling are separate

Commercial and open-source products may help organizations create, manage, validate, publish, monitor, or synchronize their files.

Those products are implementations of the standard, not part of the standard itself.

The success of `company.json` should not depend on the success of any one implementation.
