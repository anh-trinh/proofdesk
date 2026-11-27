# Contributing

## Workflow

1. Open or pick an issue.
2. Branch from `main`: `feat/<issue>-<short-name>` (or `fix/`, `docs/`, `chore/`).
3. Write the test first. Commit the failing test (`test:`), then the code (`feat:`).
4. Open a draft pull request. The PR title must follow Conventional Commits because it
   becomes the commit message on `main` (squash merge).
5. Run `make check` before marking the PR ready. It runs the same checks as CI.

## Conventional Commits

`feat:` new behaviour, `fix:` bug fix, `test:` tests only, `refactor:` no behaviour change,
`docs:` documentation, `ci:` workflows, `chore:` tooling.

## Signed commits

The ruleset requires signed commits on `main`. Sign the commits on your branch too, so
every commit in a pull request shows as Verified and the history is known to come from the
account owner.

Set these four keys once (use the path of your own SSH signing key):

```bash
git config --global gpg.format ssh
git config --global user.signingkey ~/.ssh/<your-signing-key>.pub
git config --global commit.gpgsign true
git config --global tag.gpgsign true
```

Add the public key to GitHub as a signing key (`gh ssh-key add <key>.pub --type signing`).
To check a commit after pushing:

```bash
gh api repos/anh-trinh/proofdesk/commits/<sha> --jq .commit.verification
```

`"verified": true` means GitHub accepts the signature. If it is `false`, read the `reason`
field.

## Labels

Every issue has one `type:*` label. Add `area:*` labels for the parts it touches.

| Label | Colour | Meaning |
| --- | --- | --- |
| `type:feat` | existing | New behaviour |
| `type:fix` | existing | Bug fix |
| `type:chore` | existing | Tooling and maintenance |
| `type:ci` | existing | CI workflows |
| `type:docs` | existing | Documentation only |
| `area:python` | `3572a5` | Python service code |
| `area:infra` | `ff9900` | AWS CDK and infrastructure |
| `area:web` | `1d76db` | TanStack Start web app |
| `area:docs` | `0075ca` | Documentation |
| `area:ci` | `6f42c1` | GitHub Actions and checks |
| `risk:trust-boundary` | `b60205` | Touches a trust boundary: also run `/security-review` |
| `needs:human` | `fbca04` | Has a step only the operator can do |
| `manual-test` | `0e8a16` | Manual test session for a milestone |

## Code design checklist

Linters check complexity, argument counts and naming style. These rules need a person:
reviewers and the `code-reviewer` subagent both use this list.

- A function does one thing, at one level of abstraction.
- Extract a function only when its name and interface are simpler than its body. There is
  no line limit.
- Command-query separation: a function either changes state or returns a value, not both.
- No flag arguments. Use two functions or an enum instead of a `bool` that switches
  behaviour.
- Type names carry no noise words (`Manager`, `Processor`, `Data`, `Info`) and no
  encodings (`IStore`, `str_name`).
- No SDK request or response object crosses into the domain.
- Errors are translated at the adapter into domain errors and are never swallowed.
- One behaviour per test, laid out as arrange, act, assert.

## Rules

- No secrets, no real documents, no `float` for money.
- New behaviour needs a test. Coverage must stay at or above 90%.
- Architecture decisions go in `docs/decisions/` as MADR 4.0.0 records, in the same PR as
  the change they explain.
