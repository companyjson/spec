# company.json

An open proposal for publishing first-party organization information on the web.

## Status

Early draft. The specification is not yet stable and may change based on implementation experience and public feedback.

## Website

https://companyjson.org

## Goals

- Simple
- Open
- Interoperable
- Explicitly versioned
- Easy to implement

## Current repository structure

- `SPECIFICATION.md`
- `WHY.md`
- `GOALS-AND-NONGOALS.md`
- `PRINCIPLES.md`
- `DECISIONS.md`
- `docs/FAQ.md`
- `docs/REFERENCE-IMPLEMENTATION.md`
- `schema/` — formal JSON Schema for version 0.1
- `examples/` — live reference profiles (System Three Resins, MTN Coat)
- `tools/resolver.py` — reference resolver (discovery, binding, mutual-declaration evaluation)
- `tools/tests/` — live integration suite, plus resolver binding and relationship-reciprocity edge-case tests
- `site/` — companyjson.org

## Planned

- Formal conformance test corpus (positive/negative fixtures against the JSON Schema)

## Project documents

- [Why company.json?](WHY.md)
- [Goals and non-goals](GOALS-AND-NONGOALS.md)
- [Principles](PRINCIPLES.md)
- [Project decisions](DECISIONS.md)
- [Frequently asked questions](docs/FAQ.md)
- [Reference implementation](docs/REFERENCE-IMPLEMENTATION.md)
  
## License

MIT
