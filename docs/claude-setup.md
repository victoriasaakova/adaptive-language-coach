# Claude setup

Claude and ChatGPT use the same `SKILL.md`, `references/`, templates, schema and private state. Keep one shared skill. Install this folder using the skill mechanism supported by the Claude environment, or provide it as project context and explicitly ask Claude to follow `SKILL.md`. Skill discovery depends on the host.

Keep the learner's `private/` folder outside public sources. With local read/write access, the agent maintains and verifies records. In a read-only project, give it the latest private state and expect a consolidated `UNSAVED` export; uploaded sources are not automatically writable. Do not assume a new conversation has the latest records.

Check one practice run against [behavioral scenarios](../tests/scenarios.md): all blocks including independent sentences, writing and mini-test; speaking cap; full learner-facing Markdown note and next-lesson context; no pronunciation score from text. The same acceptance criteria apply to ChatGPT.

Reminders are a separate host feature and require an explicit user request. A scheduled prompt does not guarantee an interactive lesson or saved records.
