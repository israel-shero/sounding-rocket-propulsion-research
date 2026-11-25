# Repository agent instructions

## Permanent branch policy

- `dev` is the primary development and integration branch. Start task branches from `dev` and target ordinary development pull requests to `dev`. Tested, scoped changes may be merged into `dev` without a separate owner approval for each merge, subject to existing GitHub permissions, required checks and review rules. Never bypass protections or approve your own PR to satisfy required review.
- `main` is the stable milestone branch. Promote coherent, tested integration milestones from `dev` to `main` by a deliberate pull request requiring owner approval. Do not make routine development commits to `main`.
- Preserve both permanent branches and their history. Do not force-push, delete either branch, or change permissions or rulesets without explicit authorization.
