# Optional Notion synchronization

This is an agent procedure, not an installed integration or a background sync service. The local Markdown/JSON artifacts are the source of truth. A host with an authenticated Notion connector is required. No API keys belong in configuration or Git.

The optional `notion` object is allowed only in `private/config.json`, never in `config/example.json`. Default is disabled, destination is null, and write approval is always explicit. A configured destination or enabled flag alone does not authorize access or publication.

When the learner explicitly asks to sync:

1. Read the private destination and scope. If missing, request the target page/database. Do not guess or create a workspace structure.
2. Prepare the exact lesson payload and proposed destination for review. Only share lesson content requested by the user; omit the profile and unrelated historical data.
3. Obtain a separate explicit command approving that concrete payload and destination before a write, unless the current command already unambiguously authorizes those exact contents and destination.
4. Inspect destination capabilities and existing entries through available tools. Store a local mapping `private/notion-sync.json` from lesson ID to remote page ID and content hash. Search for the lesson ID before a first create, including after an uncertain response.
5. Create once or update the mapped record. Never delete unrelated content. If remote content changed independently, show the conflict and request a resolution.
6. Verify the response/readback, then save the mapping, timestamp and hash locally. On failure preserve local artifacts, report unsynced status and stop; do not blindly retry an ambiguous write or claim success.

If no connector is available, produce a manual Markdown export and explain that no sync happened. Never enable sync as a side effect of starting a lesson.
