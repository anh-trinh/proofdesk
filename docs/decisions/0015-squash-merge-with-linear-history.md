---
status: accepted
date: 2026-11-19
decision-makers: Anh Trinh
---

# Merge pull requests by squash, with a linear history on main

## Context and Problem Statement

Every change reaches `main` through a pull request. PR #3 was merged with rebase, which put
seven separate commits on `main`, while PR #4 was squashed with a title that is not a
Conventional Commit. The repository needs one merge method, so that `main` is predictable
for `git bisect`, for reverts, and for release-please, which builds the changelog from the
commits on `main`.

## Decision Drivers

* Every commit on `main` builds and passes the tests
* One commit on `main` per reviewed change, with a Conventional Commits message
* Commits on `main` are signed and show as Verified on GitHub
* The TDD sequence (`test:` then `feat:`) stays visible to a reviewer

## Considered Options

* Squash merge
* Rebase merge
* Merge commit

## Decision Outcome

Chosen option: "Squash merge", because it gives exactly one green, signed commit on `main`
per pull request, and the PR title becomes that commit. Rebase and merge commits are
disabled in the repository settings, and the `main` ruleset requires a linear history.

### Consequences

* Good, because `main` maps one commit to one reviewed PR, and `git revert` of a feature is
  one command.
* Good, because the PR title check in CI and release-please work on the same text.
* Bad, because the individual `test:` and `feat:` commits are not on `main`. They remain in
  the Commits tab of each merged PR, which is where the TDD history is shown to reviewers.
* Bad, because commits already on `main` from before this decision (PR #3 and PR #4) do not
  follow it. History on `main` is not rewritten, since that needs a force push to a
  protected branch.

### Confirmation

The repository allows squash merge only. The `main` ruleset requires a linear history,
signed commits and a passing `pr-title` check.

## Pros and Cons of the Options

### Rebase merge

* Good, because every commit of the PR is kept on `main`.
* Bad, because GitHub cannot sign rebased commits, and red `test:` commits would land on
  `main`, which breaks `git bisect`.

### Merge commit

* Good, because the full branch history is preserved.
* Bad, because the history is not linear and the merge commit message is not a Conventional
  Commit.

## More Information

**Deviation from the playbook on AI attribution.** The playbook (sections 4.8 and 12.5)
keeps the Claude Code `Co-Authored-By` trailer on commits. This repository does not add the
trailer. The use of Claude Code is disclosed instead in [AI-assisted workflow](../ai-workflow.md),
which describes what the agent did, what the operator decided, and the checks around it.
