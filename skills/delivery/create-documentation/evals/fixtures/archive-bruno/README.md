# Synthetic archive collection

This is a collection fixture for documentation evaluation, not a deployed API. The authoritative fictional contract is the sibling archive-jobs.md. Requests and assertions are declared scenarios, not observed results. No request has been run.

Read bruno.json and Sandbox.bru first, then the request docs. The host is example.test. Supply credentials and fixture-dependent IDs only for an authorized test service. No login, refresh, cancellation, simulation, or state-changing read route exists. Tokens and missing/cursor fixture values are deliberately empty.

There are 20 request cases across 3 method/path operations. Cases cover supported errors, explicit null/omitted/empty/non-empty labels, all four job states, and pagination. State and empty-list cases require externally prepared data. They do not create that state. A write may enqueue work again when repeated; there is no idempotency support.

External source gaps remain: no application implementation, Git history for the fictional service, plan, machine-readable Swagger/OpenAPI document, or live server is supplied. The fixture contract supplies intended behavior. Running this collection needs a real compatible test service and prepared data, neither of which is included.
