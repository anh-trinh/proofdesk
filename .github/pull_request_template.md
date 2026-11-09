## Change
- Related issue:
- Plan agreed before coding: yes / no

## Quality
- [ ] Test written first and seen failing before passing
- [ ] Coverage did not drop
- [ ] No float used for money
- [ ] Contracts (JSON Schema, TS types) regenerated if a model changed

## Security
- [ ] No secrets, no real data
- [ ] IAM not widened, no `*`
- [ ] Input from users and from the model is validated
- [ ] tenantId comes from the session, not from the request
- [ ] Logs contain no extracted values or PII
- [ ] New dependency (if any) checked for licence and vulnerabilities

## AI (only if prompt or model changed)
- [ ] Evaluation run, report link:
- [ ] Recorded in evals/CHANGELOG.md
- [ ] Tokens and cost per document before and after:

## AI-generated code
- [ ] I read every line of the diff
- [ ] I can explain every line if asked

## Review
- [ ] PR title follows Conventional Commits
- [ ] Ran /code-review (and Copilot if enabled), handled every comment
