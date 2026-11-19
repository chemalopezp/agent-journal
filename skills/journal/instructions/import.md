# Import

When the person brings in notes or files from another app.

## Ways in

1. **Drop it in the conversation** — a few notes, pasted text, screenshots, a small file. Process right away.
2. **Drop it in `sources/<source>/_raw/`** — bulk exports (e.g. an unzipped Google Takeout). Process on request or at the next run.

## Large imports (hundreds or thousands of items)

Don't read items one by one in conversation. Use a script, then triage in batches.

1. Run the converter as a **dry run** and show the person the report (counts, years, labels, flagged).
2. After approval, run it with `--write`. Notes land in `sources/<source>/`, not the inbox.
3. Triage in batches (by label or by year), not per note: propose where each group goes, plus a few notes worth promoting into the right scope (records, plans).
4. Leave the rest in `sources/` — it's searchable archive, not a to-do list. Distilled notes link back to their source.

Scripts: `engine/connectors/import_keep.py` (Google Keep), `engine/connectors/import_gemini.py` (Gemini activity).

## Steps

1. **Inventory.** List what's there: count, types, date range. If more than 20 items, show the plan and wait for approval.
2. **Convert** each item to a new file: `sources/<source>/YYYY-MM-DD-HHmm-<slug>.md` (a few items from a conversation can be filed straight into their scope), using the item's **original** creation date.

   ```yaml
   ---
   type: import
   source: google-keep | text | pdf | image | <app>
   source_id: <original id or file name>
   original_created: YYYY-MM-DD
   created: <today>
   author: <agent>
   tags: [<original labels>]
   ---
   ```

   Body:

   ```markdown
   ## Original
   <content, verbatim; checklists as - [ ] / - [x]>

   ### 🤖 <agent> · import · YYYY-MM-DD HH:mm
   Summary: one line
   Suggested home: <scope> · <type>
   Suggested links: [[…]]
   ```

3. **Attachments** go to `sources/attachments/<source>/` and are linked from the note.
4. **Skip:** trashed items, empty items, exact duplicates (same content). Count them.
5. **Sensitive content:** add `sensitive: true` and flag it. **Secrets** (passwords, keys, account numbers): don't import; list them for the person.
6. **Raw files:** never delete. Move processed files to `sources/<source>/_raw/done/`.
7. **Report** in a session note (or the day note, for a scheduled import): imported N from <source> · skipped M (trashed, empty, duplicate) · flagged K · next step.

Distilling into records and plans happens later, in batches, after the person approves.

Documents (statements, contracts, PDFs worth keeping) follow `instructions/documents.md` instead: original outside the vault, card in the scope's `records/` (`type: document`).

## Source notes

### Google Keep

Export with Google Takeout (select only Keep). Each note comes as a `.json` (plus `.html`). For a full export use the script:

```
python3 engine/connectors/import_keep.py <Takeout/Keep> <vault>           # dry run
python3 engine/connectors/import_keep.py <Takeout/Keep> <vault> --write
```

It skips trashed, empty and duplicate notes, withholds the content of notes that look like they contain secrets (and lists them), copies attachments and writes a report. Useful JSON fields:

| Field | Use |
|---|---|
| `title`, `textContent` | Title and body |
| `listContent[].text`, `.isChecked` | Checklist items |
| `labels[].name` | Tags |
| `isTrashed` | Skip if true |
| `isArchived`, `isPinned` | Add tags `archived-source`, `pinned-source` |
| `createdTimestampUsec` | `original_created` (microseconds since epoch) |
| `attachments[].filePath` | Copy to `sources/attachments/google-keep/` |

### Gemini (My Activity)

Export with Google Takeout → My Activity → Gemini Apps. You get one large `My Activity.html` plus attachments.

```
python3 engine/connectors/import_gemini.py "<…/My Activity/Gemini Apps/My Activity.html>" <vault>           # dry run
python3 engine/connectors/import_gemini.py "<…/My Activity/Gemini Apps/My Activity.html>" <vault> --write
```

Writes one file per month to `sources/gemini/YYYY-MM.md`: each entry with date, the prompt in full and the response in a collapsed callout. Attachments are not imported. Entries that look like they contain secrets are withheld.

After writing, the agent adds a summary block at the top of each month (topics, projects, people, decisions) and proposes a few notes to promote into the right scope. The person approves before anything is filed.

### Plain text / markdown

Keep as-is under `## Original`. Take the date from the file or the content if present; otherwise use today and say so.

### PDF / images

Store the file in `sources/attachments/<source>/`. The note holds a short summary and the link. Don't transcribe sensitive documents.
