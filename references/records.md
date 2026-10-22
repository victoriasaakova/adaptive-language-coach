# Records and spaced repetition

All live learner data belongs in `private/`. Treat public examples as fiction. Resolve paths relative to the repository/skill root, not the process's current directory.

## Incremental recording owned by the agent

Create missing files after onboarding without asking the learner to fill them. After introducing an expression, add it to vocabulary with its actual introduction date, models and pending review milestones; introduction alone is not successful use. After learner answers, append actual examples, assistance flags, errors and review outcomes. Assign each observation a stable lesson ID + block + attempt ID and store that identifier alongside the evidence to avoid duplicates when retrying writes or resuming. Error recurrence counts represent distinct observed attempts, not repeated processing of one answer.

After each completed block, update the partial lesson note, provisional progress and checkpoint. Mark a block completed only after its responses are recorded. Do not interrupt teaching with file dumps or requests to “save this”; perform authorized local writes quietly and verify them. On a write failure, retain pending changes in the current context, report unsaved status briefly and retry only after checking what actually persisted. Per-file atomic replacement is not a cross-file transaction: reconcile observation IDs across the note, vocabulary, errors and checkpoint before resuming. Never mark the checkpoint ahead of saved evidence.

At lesson close, reconcile all records, finalize evidence-based scores and update `private/learning-plan.md` for the next lesson. This does not require manual entry or repeated permission for ordinary local learning records. Notion remains separately authorized. Without a writable store, maintain an in-chat draft and return one consolidated export containing the profile, plan, vocabulary, errors, progress, checkpoint and latest note. Label it UNSAVED; do not claim that it updates Project sources or survives a new chat automatically.

## Local artifacts

The learner-facing note and next-lesson context are required at every handoff; follow [lesson handoff](lesson-handoff.md). Link or display the full note rather than claiming that a short recap is the complete record.

- `private/learning-plan.md`: agent-built goals-to-situations mapping, learner-chosen week horizon or provisional range, start/target window, weekly milestones with observable checks, lesson cadence, topic rotation, diagnostic needs, per-skill provisional baseline, 15/30-minute task structure and next focus; update evidence and upcoming tasks after lessons without silently changing the user's end goal or deadline.
- `private/lessons/YYYY-MM-DD-NN.md`: one note per lesson, using `templates/lesson.md`; never overwrite another same-day lesson. Use `lesson_id` as the idempotency key when resuming.
- `private/errors.md`: append observed errors with lesson ID, original, correction, rule, severity, recurrence count, last seen and status (open/practicing/stable). Repeated patterns update an existing entry; retain dated evidence. “Stable” requires successful later use.
- `private/vocabulary.json`: array of vocabulary objects described below.
- `private/progress.md`: per-lesson evidence table (dimension, score or N/O, sample, confidence), first-attempt mini-test, target-expression coverage, observed trends and next priority. No invented baseline. Maintain a separate diagnostic baseline for writing, speaking and grammar: provisional estimated band or insufficient evidence, source samples/lesson IDs, assistance, confidence, date, and next diagnostic need; preserve the original self-report separately.
- `private/checkpoint.json`: lesson ID, date, topic, duration, modality, completed/reduced/pending blocks, target expressions and next prompt. Clear active status only when closed; retain partial status if interrupted.

Use `templates/state.md` to initialize empty error/progress records. Never silently replace a malformed existing file. Preserve old data, report the issue and provide a proposed repaired artifact. For structured writes, write a temporary sibling and atomically replace after validation; read it back. In chat-only mode emit the same named artifacts as text or downloads with `UNSAVED` status. At the next lesson request the latest state if not accessible.

## Vocabulary contract

Each entry contains `id` (stable unique string), `language`, `expression`, `meaning`, `register`, `model_sentence`, `learner_examples` (dated original attempts and corrections), `introduced_on` (local ISO date), `passed_offsets` (unique subset of [1,3,7,14]), `retry_on` (ISO date or null), `reviews` (date, result, assisted, evidence), and `status` (`learning` or `cycle_complete`). Do not put answers in the recall prompt. Deduplicate by language + normalized expression while preserving legitimate distinct senses with separate IDs.

## Deterministic D+1/3/7/14 policy

D is the introduction date in the configured IANA timezone. Initial target dates are D+1, D+3, D+7 and D+14 calendar days; these are not day gaps compounded after each success. Use `scripts/srs.py` for date calculation when Python is available, or apply the same algorithm manually.

At lesson start, select entries with next due <= today, oldest due first; cap recall at 3 / 5 items and carry the rest as a visible backlog. Never mark omitted entries reviewed. A missed session doesn't count as failure and does not mark overdue stages passed.

An unassisted correct retrieval **and** meaningful novel use qualifies as a pass. An incorrect, hinted or imitated answer does not. On failure, log the attempt and set `retry_on` to the next calendar day. Do not advance a stage or erase previous successes. A same-day retry is practice only. On a successful due retry, pass only the earliest still-unpassed original milestone whose date has arrived, clear retry, and leave later milestones pending. If additional milestones are already overdue, next due becomes the day after the latest actual review; never complete several stages from one response or cram stages in the same day. An early correct practice does not advance a milestone. Failed early practice still schedules a next-day retry.

After all four milestones pass, mark `cycle_complete`, not permanent mastery; use occasional transfer checks in later lessons. If a later check fails, reset passed offsets and introduction date to that failure date, set next review to D+1, retain all historical reviews, and mark learning.

Dates and review results must come from observable attempts and known local dates. No background review or notification is implied.
