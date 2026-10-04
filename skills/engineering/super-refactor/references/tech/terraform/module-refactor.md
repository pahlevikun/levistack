# Terraform module refactor mode

Scoped mode — not general application refactoring.

## Inputs to clarify

- Source directory
- Module name
- Abstraction level (simple / intermediate / advanced)
- Whether state must stay compatible (`preserve_state`)
- Target registry (local / private / public)

## Phases

### 1. Analysis

- Group resources by function
- Find repeated patterns and dependencies
- Map variable propagation and cross-resource references
- Assess state migration complexity (`terraform state list`, `terraform show -json`)

### 2. Module design

- Clear variable objects with validation
- Outputs as the module contract
- Include tightly coupled resources; keep cross-cutting tags/monitoring explicit at root when lifecycles differ

### 3. Migration

- Plan state moves before apply
- Document upgrade path for callers
- Verify plan/apply in a safe environment

Behavior-preserving for infrastructure means **same effective resources** unless user scoped replacement.
