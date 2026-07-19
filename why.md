# Why company.json?

Organizations publish the same basic information about themselves in many places:

- About pages
- Website footers
- Press and media pages
- Structured data embedded in webpages
- Social profiles
- Investor-relations sites
- Partner portals
- Business directories
- Third-party databases

These sources frequently disagree, become outdated, or require a person or machine to infer which information is official.

Humans can browse several pages, compare sources, and make judgment calls. Software systems often have to crawl unstructured pages, interpret inconsistent terminology, and guess which source should be trusted.

There should be a simpler option.

## The proposal

`company.json` is an open specification for publishing an organization's public information in a predictable, machine-readable format.

The file is published on a domain controlled by the organization and can contain information such as:

- Organization name
- Legal name
- Description
- Official website
- Logos
- Contact information
- Locations
- Leadership
- Brands
- Social profiles
- Press and investor-relations resources
- Date last modified

The file represents information the organization is intentionally publishing about itself.

It does not require a proprietary platform, central registry, commercial account, or third-party API.

## Why now?

The web is increasingly consumed by software as well as people.

Search engines, AI systems, browsers, agents, directories, procurement systems, partner platforms, and other services routinely need basic information about organizations.

Today, these systems typically extract that information from webpages or obtain it from third-party databases. Both approaches can produce incomplete, inconsistent, or outdated results.

`company.json` gives organizations a direct way to publish the public facts and resources they want machines to use.

AI is an important catalyst for this work, but `company.json` is not an AI-specific format. It is intended to remain useful regardless of which search engines, AI models, browsers, or software platforms become dominant.

## Why not just use an About page?

About pages are designed primarily for people.

Their structure, language, and content vary significantly from one website to another. A human can usually interpret them, but software must extract meaning from headings, prose, navigation, and page layout.

An About page can remain the best human-facing presentation of an organization.

`company.json` provides a complementary machine-readable representation.

## Why not just use Schema.org?

Schema.org provides a widely used vocabulary for describing organizations and many other kinds of entities.

`company.json` should complement and reuse Schema.org concepts wherever practical rather than create a competing vocabulary.

The distinction is one of publication and discovery:

- Schema.org defines shared terms and meanings.
- `company.json` defines a predictable, standalone, first-party organization profile.

A tool should eventually be able to generate both Schema.org markup and `company.json` from the same underlying information.

## Why not use a central company database?

Third-party databases can be valuable, but they introduce several limitations:

- The organization may not control the record.
- Updates may take time to propagate.
- Different databases may contain conflicting information.
- Access may require a paid account or proprietary API.
- The database operator becomes a central dependency.

With `company.json`, the organization publishes the source directly on a domain it controls.

Independent services may still index, normalize, verify, or enrich that information, but the public profile does not depend on any one service continuing to exist.

## Is the information verified?

`company.json` is a first-party publication mechanism, not an independent certification system.

A valid file means that the file follows the specification. It does not prove that every claim in the file is factually correct.

Consumers remain responsible for deciding how much trust to place in first-party claims and whether additional verification is required.

## Why call it company.json?

The filename is intentionally direct and easy to remember.

Although the word "company" is used, the specification is intended to support many kinds of organizations, including:

- Businesses
- Nonprofits
- Schools and universities
- Healthcare organizations
- Associations
- Public institutions
- Open-source organizations

The filename is a practical web convention, not a statement about an organization's legal form.

## What success looks like

The project succeeds if:

- Organizations can publish a valid file without using a particular vendor.
- Developers can implement the specification from the documentation alone.
- Website platforms and content-management systems can generate it automatically.
- Browsers, AI systems, search engines, directories, and other tools can consume it.
- The specification remains small enough to understand and implement easily.
- The format becomes useful without requiring people to think about the format itself.

The long-term goal is not to make `company.json` visible.

The goal is to make authoritative public organization information easier to publish, discover, and reuse.

## Project status

`company.json` is currently an early draft.

The specification, examples, discovery mechanism, and field definitions are expected to change based on implementation experience and community feedback.
