# Configuration contract

`config/schema.json` is JSON Schema Draft 2020-12. `config/example.json` is an intentionally fictional profile. `private/config.json` is a complete user configuration, not a partial merge or an overlay. Explicit session requests override duration/topic for that session only; do not rewrite permanent preferences without a request.

The agent populates this configuration from a short onboarding conversation. Users do not need to edit JSON or supply a lesson protocol. This schema is for agent validation and maintainers. Existing configurations are completed conversationally, never reset.

Required fields:

| Field | Meaning |
|---|---|
| schema_version | Exactly 1 |
| native_language / target_language | Language name or code; must differ |
| level.self_reported / goal | Ask for approximate starting level (allow `unknown`) and desired level; not certified scores |
| goals | At least one learner-defined communicative objective; clarify what they want to do with the language |
| interests | At least one topic selected by the learner; ask during onboarding rather than assume |
| context.life / context.work | Arrays of practical situations; at least one must be nonempty. Work may be empty if irrelevant or declined. No identifying details needed |
| session.default_minutes | 15 or 30 |
| session.preferred_time | Descriptive preference; not a scheduler |
| session.timezone | Valid IANA timezone for calendar-day repetition |
| session.mode | auto, text or voice; capability checks still apply |
| feedback.style | precise or supportive; both retain the same scoring criteria |
| feedback.automatic_praise | Must be false; earned, specific feedback is allowed |
| feedback.explanation_language | Language for brief explanations |

Optional private-only `notion`: enabled (boolean), destination (nonempty page/database reference or null when disabled), require_explicit_write_approval (must be true). No token/password fields. An enabled configuration requires a destination but still requires an explicit write instruction. Public example validation rejects the whole Notion object.

`python scripts/validate.py` validates the public example. `python scripts/validate.py --private private/config.json` additionally validates a private profile locally. Validation includes timezone resolution and distinct source/target identifiers, beyond JSON Schema. Semantic aliases (e.g. “English” and “en”) require agent judgment. Unknown properties are errors to catch typos.

Missing or invalid configuration: explain the field-level issue without printing the complete personal profile; ask for missing information or a correction. Do not guess a target language from the repository name, examples or interface language.
