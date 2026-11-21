# AI-assisted workflow

ProofDesk is built with Claude Code. This page explains how the agent is used, what it is
allowed to do, and how its output is checked, so a reader can judge the process and not
only the code.

## Tools

| Tool | Use |
| --- | --- |
| Claude Code (desktop app and CLI) | Planning, writing code and tests, opening issues and pull requests, local review |
| Claude Opus 5.5 | Main model for planning and implementation |
| `/code-review --comment` | Second review of each pull request, posted as PR comments |
| `/security-review` | Extra review for changes that touch a trust boundary, such as parsing uploaded XML |

## Who does what

The project is run as AI-assisted development with a human reviewer. The agent does the
hands-on work, and the operator (Anh Trinh) owns every decision.

| The agent | The operator |
| --- | --- |
| Proposes a plan in plan mode, before any file changes | Approves, changes or rejects the plan |
| Opens issues with acceptance criteria | Agrees on scope and priorities |
| Writes the failing test, then the code, in separate commits | Reviews every pull request diff |
| Runs `make check` and pastes the command output into the PR | Approves a pull request before it is merged |
| Applies repository settings that are stored in the repository, such as the ruleset | Approves each settings command through the permission prompt |
| Records decisions as ADRs in the same pull request | Accepts the decision and any deviation from the playbook |

The agent never runs `cdk deploy`, never deletes AWS resources, and never reads `.env` files
or `samples/private/`. These limits are enforced by Claude Code, not only written down.

## Guardrails

Rules that must hold every time are enforced by tools, because instructions in `CLAUDE.md`
are guidance that the model may judge not to apply.

| Guardrail | Where | What it stops |
| --- | --- | --- |
| Deny rules | [`.claude/settings.json`](../.claude/settings.json) | Reading secrets and private samples, `cdk deploy`, deleting AWS data |
| Project rules | [`CLAUDE.md`](../CLAUDE.md) | Money as `float`, XML without `defusedxml`, `*` in IAM, `tenantId` from the request, personal data in logs |
| Pre-commit hooks | [`.pre-commit-config.yaml`](../.pre-commit-config.yaml) | Secrets, private keys and unformatted code before a commit exists |
| CI and the `main` ruleset | [`.github/workflows/`](../.github/workflows/), [`.github/rulesets/`](../.github/rulesets/) | Merging without green tests, coverage of at least 90%, a Conventional Commits title, and resolved review threads |
| Code scanning | CodeQL, dependency review, OpenSSF Scorecard | Known vulnerability patterns, vulnerable dependencies, weak repository settings |

## Task loop

1. **Issue:** each change starts as an issue with Given, When, Then acceptance criteria.
2. **Plan:** the agent reads the code and proposes a plan. Nothing is edited until the
   operator approves it.
3. **Red:** the agent writes the test from the acceptance criteria, runs it, and commits it
   only after it fails for the expected reason (`test:` commit).
4. **Green:** the smallest code that passes, in its own commit (`feat:` or `fix:`), then an
   optional `refactor:` commit with the tests still green.
5. **Evidence:** `make check` output, including the failing run from step 3, goes into the
   pull request description. "All tests pass" without output is not accepted.
6. **Independent review:** `/code-review --comment` runs in a fresh context that did not
   write the code. Each finding is fixed in its own commit or answered with a reason.
7. **Human review and merge:** the operator reads the diff and approves. The pull request
   is squash merged ([ADR-0015](decisions/0015-squash-merge-with-linear-history.md)).

## Known gaps in the early history

The process above was adopted on 19 November 2026. Commits before that date show the
learning curve and are kept as they are, because rewriting `main` would need a force push to
a protected branch.

- The first commit is GitHub's `Initial commit`, and PR #4 was merged with the title
  `docs/review rules`. Neither follows Conventional Commits. A CI check on PR titles now
  prevents this.
- PR #3 was rebase merged, so its seven commits are on `main` individually. Later pull
  requests are squash merged.
- Commits before 19 November 2026 are not signed.

## Where the process caught the agent

- **Unverified test evidence (PR #25).** The first description quoted a YAML validation
  command that had not been run, and the command would have failed because PyYAML is not
  installed. The operator rule that evidence must be real output caught it, and the
  description was corrected to the `pre-commit run check-yaml` output that actually ran.
- **ADR number collision (PR #31).** The squash merge decision was first numbered ADR-0002,
  which the handbook reserves for the polling decision. A check against the handbook's ADR
  list caught it, and the record was renumbered to ADR-0015 in a follow-up commit instead of
  rewriting the pushed branch.
