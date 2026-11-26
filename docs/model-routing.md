# Model and effort routing

Which Claude model and effort level each kind of task uses in this repository, and why.
A stronger model and a higher effort use more of the plan, so the choice is made per task
type and every plan states it.

Checked on 26 November 2026 against the Claude Code documentation:

- [Model configuration](https://code.claude.com/docs/en/model-config)
- [Subagents](https://code.claude.com/docs/en/sub-agents)
- [Skills](https://code.claude.com/docs/en/skills)

On that date `sonnet`, `opus` and `haiku` resolve to Sonnet 5.5, Opus 5.5 and Haiku 5.5 on
the Anthropic API. All three accept the effort levels `low`, `medium`, `high`, `xhigh` and
`max`, and all three default to `medium`. Haiku 5.5 needs Claude Code v2.1.293 or later.
Aliases move to newer models over time, so re-check this page when a new model ships.

## Routing table

| Task type | Model | Effort | Reason |
| --- | --- | --- | --- |
| Routine edits and docs | `sonnet` | `medium` | Fast and light on usage; the work is low risk |
| Well-scoped feature with tests | `sonnet` | `high` | Enough depth for test-first work without Opus cost |
| Security, CI/CD, IAM, infrastructure | `opus` | `high` | A mistake here is hard to undo |
| Bug fixes and debugging | `opus` | `high`, then `xhigh` after one failed attempt | Needs reasoning across several files |
| Architecture spikes and ADRs | `opusplan` | `high` | Opus plans and weighs trade-offs, Sonnet carries out the edits |
| Review: `code-reviewer` | `sonnet` | `high` | Independent, read-only review of a diff |
| Review: `security-reviewer` | `opus` | `high` | Independent, read-only review of trust boundaries |
| Docs help: `docs-helper` | `haiku` | `medium` | Wording and links under `docs/` only |

The review rows match the `model` and `effort` in the frontmatter of
[`.claude/agents/`](../.claude/agents/). The `manual-test-guide` skill uses `sonnet` and
`medium`, and `new-adr` uses `opus` and `high`; see [`.claude/skills/`](../.claude/skills/).

What the documentation says for the values in the table:

- Aliases: `opusplan` is a "special mode that uses `opus` during plan mode, then switches to
  `sonnet` for execution" (Model configuration).
- Subagent `effort` accepts `low`, `medium`, `high`, `xhigh` or `max`, and "available levels
  depend on the model" (Subagents).
- Skill `effort` takes the same five levels and "overrides the session effort level"
  (Skills).

## Commands

| Command | What it changes |
| --- | --- |
| `/model <alias>` | Switches the model for the session. In the picker, `Enter` saves it as your default and `s` applies it to this session only |
| `/effort` | Sets the effort level. In the slider, `Enter` saves the level as the default for that model and `s` applies it to this session only |
| `claude --effort <level>` | Sets the effort level for one launch |
| `opusplan` | Uses Opus in plan mode and Sonnet for execution |
| `ultrathink` | Asks for deeper reasoning on one turn. It does not change the effort level the session sends to the API |

The environment variable `CLAUDE_CODE_EFFORT_LEVEL` overrides every other setting. A
subagent or skill `effort` does not override it. `max` applies to the current session only.

## When to change the setting

- **Raise effort** when Claude skips files, tests or checks, or gives a thin plan.
- **Switch to a stronger model** when it still fails with the full context in view.
- **Fix the prompt** when the cause was missing context. A stronger model does not repair
  a prompt that left out the file or the rule.

## Cost notes

- Opus and a higher effort use more of the plan than Sonnet at `medium`. The documentation
  does not give a ratio, so this is the project's working assumption, not a measured figure.
- The `fable` alias is not used here. The documentation says that "Fable usage can bill to
  usage credits instead of drawing on your plan's included limits".
- `max` is for one session, after `xhigh` has failed.
