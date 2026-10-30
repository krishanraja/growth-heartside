# CoWork: put the approved breed examples in Google Drive

29 October 2026. Paste the prompt below into a CoWork session on Krish's computer, with the
`growth-heartside` folder shared and Google Drive connected. It copies only approved artwork. It
creates folders and uploads files in Krish's own Drive; it shares, publishes, posts or deletes
nothing.

---

You are filing Heartside's approved example artwork into Google Drive. Work only from the local
folder `~/growth-heartside` (branch `codex/heartside-examples-2026-10-29`) and Krish's Google Drive.
Never upload anything that is not approved, never share a file or folder, never delete or overwrite
anything in Drive, and never post, publish or send anything.

**The source of truth is the ledger**
`~/growth-heartside/assets/heartside-examples-2026-10-29.approvals.json`. Each entry in its
`paintings` list has `job`, `status` and `sha256`. A job is approved only when one of its entries has
`status` "approved". Rejected, superseded and pending entries are never uploaded, and nothing under
`~/growth-heartside/local/` is ever uploaded.

**Step 1. Check before uploading.** For every approved entry, compute the sha256 of
`assets/heartside-examples-2026-10-29/paintings/<job>.png` and confirm it equals the ledger's
`sha256`. Also confirm no file in `paintings/` belongs to a job without an approved entry. If any
check fails, stop and tell Krish exactly which file, and upload nothing.

**Step 2. Build the list.** From `assets/heartside-examples-2026-10-29/manifest.json`, take every
entry whose `job` is approved and whose file exists on disk: the painting, the cutout, the three crops
and the mockups. Add the job's contact sheet `contact/<job>.jpg` when it exists, the dog's photo
`photos/<dog>.jpg` (the dog is the first word of the job id), `credits.json` and the ledger itself.
Do not upload any file whose name ends in `-full.png`.

**Step 3. Create the folders** in Krish's Drive, only if they do not exist yet:

```
Heartside / Example artwork / 2026-10-29 breeds /
  <Dog name> (<breed>) /            e.g. "Maple (Golden Retriever)", from jobs.json example_name
    <job id> /
      painting / cutout / crops / mockups / contact sheet
  _photos and credits /
  _ledger /
```

**Step 4. Upload** each file into its folder under its own file name. If a file with that name is
already there, compare sizes: identical means skip it, different means stop and ask Krish. Do not
rename or convert anything.

**Step 5. Report back** with one table: dog, job, tone, style, gift, and the count of files uploaded,
skipped and missing. Then list every job in the ledger that is not approved, with its status and
reason, so Krish sees what was left out and why. Finish with the Drive folder's link.
