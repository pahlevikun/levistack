---
description: "Shared API and schema contracts live in one repository; consumers pin an immutable revision and never copy generated code."
alwaysApply: false
---

# External contracts (protobuf, OpenAPI, schemas)

When contract source and generated code belong to a standalone repository:

- **Change contracts in the owning repository,** including schema, package, service, message and generated-code changes. Run generation, lint and breaking-change checks there.
- **Do not copy** contract source or generated modules into consumers, and do not add a second in-repo contracts package or directory.
- **Pin an immutable revision:** a release tag, or a full 40-character commit SHA while integrating an untagged revision. Never a branch. Never a local `path:` dependency (a sibling checkout is reference material only).
- **Every consumer declares identical dependency options,** and the lockfile is committed after the revision changes.
- **Keep bounded-context packages separate** instead of merging them into one namespace.
- **Do not restore or consume retired compatibility contracts.**
- **Mapping stays with the consumer.** Contract-to-domain transformers live in the transport that owns the API; ownership of the contract does not move presentation mapping into it.

## Consumer workflow
1. Inspect the change in the contract repository.
2. Check whether package or generated module names changed.
3. Update every consumer's dependency spec identically.
4. Refresh only that dependency in the lockfile.
5. Build, then run focused handler and transformer tests.
6. Update API and architecture docs if services, messages or source paths changed.
