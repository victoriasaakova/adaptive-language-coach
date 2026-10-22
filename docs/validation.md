# Local validation report

Checked: 2026-10-22. Environment: Python 3.9.6, Git 2.39.5. Runtime dependencies used for checks: jsonschema 4.23.0, PyYAML 6.0.2.

## Executed

- Public example and local private profile passed Draft 2020-12 schema and semantic validation. Private values were not printed in the report.
- All **13 unit tests passed**: valid/invalid config, mandatory fields, learner-selected topics and life/work contexts, unknown starting level, private-only Notion settings, explicit approval flag, language distinction, leap-year dates, all four review milestones, overdue stages, same-day practice, hinted answers, novel use, failures/retries, cycle reopening and backdating.
- The skill-creator `quick_validate.py` accepted the SKILL.md frontmatter, name and body scaffold checks.
- Relative Markdown links resolved to existing files. Exactly one SKILL.md exists in the public manifest.
- Git ignore rules excluded private configuration and learning state. The staged public manifest contained no private paths, local absolute paths or distinctive private-profile values checked during this build.
- Public ZIP was assembled from the reviewed Git index file list, excluding private files, Git metadata, caches and the test environment. Its entries and contents were compared with that list.
- At the initial local-validation stage, no Git remote was configured and no GitHub publication had occurred. Publication may follow a separate user command. No Notion action, reminder creation or automatic lesson was part of validation.

- Generated single-file ChatGPT Project bundle matched its canonical public sources (`build_chatgpt_bundle.py --check`). Incremental recording and agent-owned setup are specified; behavioral scenarios T27–T30 remain unexecuted.

## Not executed

The 30 scenarios in `tests/scenarios.md` specify expected agent behavior. They have **not** been run as full interactive evaluations. In particular, no live 15/30-minute learner session, voice/audio assessment, ChatGPT Project account test, Notion integration test or hosted GitHub Actions run has been performed. The worked lesson is synthetic and does not establish pacing or learning outcomes.

This report verifies local packaging and deterministic logic, not guaranteed model compliance or a learner's proficiency. Before relying on daily use, run T05/T06, T09, T16 and T22 in the chosen host. Notion scenarios require separate explicit authorization before any actual write.
