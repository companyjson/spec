# Frequently Asked Questions

> **Project status:** `company.json` is an early draft. The specification, schema, discovery mechanism, and field definitions may change based on implementation experience and public feedback.

## What is `company.json`?

`company.json` is a proposed open specification for publishing authoritative public information about an organization in a predictable, machine-readable format.

The file may contain information such as:

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
- Press resources
- Investor-relations resources
- Date last modified

The organization publishes the file on a domain it controls.

## What problem does it solve?

Organizations publish the same information in many places, including About pages, press pages, website footers, social profiles, structured data, investor-relations sites, directories, and third-party databases.

Those sources often disagree or become outdated.

Humans can browse several pages and decide which information appears official. Software systems usually have to extract, interpret, and reconcile information from many different sources.

`company.json` gives an organization a direct way to publish the public facts and resources it wants machines and other consumers to use.

## Who is `company.json` for?

Potential publishers include:

- Businesses
- Nonprofits
- Schools and universities
- Healthcare organizations
- Associations
- Public institutions
- Open-source organizations
- Other organizations with a public web presence

Potential consumers include:

- Browsers
- Search engines
- AI systems and agents
- Journalistic tools
- Directories
- Procurement platforms
- Partner systems
- CRM and enrichment tools
- Content-management systems
- Organization-profile viewers

The specification is not designed exclusively for any one type of publisher or consumer.

## Why is it called `company.json` if nonprofits and schools can use it?

The filename is intended to be direct, memorable, and easy to guess.

In this context, “company” is a practical web convention rather than a claim about the publisher’s legal structure.

The data model is intended to support many kinds of organizations, including nonprofits, educational institutions, healthcare organizations, associations, and public institutions.

## Is a JSON file just a text file?

Yes. JSON is a structured text format.

The structure allows software to understand the meaning and type of each value without trying to infer them from prose or webpage layouts.

For example:

```json
{
  "name": "Example Organization",
  "url": "https://example.org"
}
