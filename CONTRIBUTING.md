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

## Rules

- No secrets, no real documents, no `float` for money.
- New behaviour needs a test. Coverage must stay at or above 90%.
- Architecture decisions go in `docs/decisions/` as MADR 4.0.0 records, in the same PR as
  the change they explain.
