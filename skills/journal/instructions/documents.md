# Documents

Keeps the **document catalog**:

| Layer | Where | What |
|---|---|---|
| Originals | `documents_root` (outside the vault, e.g. a personal cloud drive) | The files. Never edited, never deleted |
| Text copies | Next to each original (`<file>.txt`), or in a local cache when originals are read-only | Plain text, so originals can be searched without opening each one |
| Cards | The scope's `records/` (`type: document`) | One note per original: what it is, what it contains, what's been extracted |

Cards are an index. They're never the full truth: the original is.

## Add a document

1. Save the original under `documents_root`, in `<year>/<category>/` (or the person's existing folders). Never overwrite; add `-2` if the name exists.
2. Create the text copy (PDF text, or OCR for scans if available): next to the original if you can write there, otherwise in a local cache outside the vault.
3. Create the card `<scope>/records/<doc-date> <title>.md` from the `document` template:
   - **Summary** — 2–3 lines.
   - **Contains** — a table of contents of what's in it, even parts not needed now.
   - **Extracted** — only what the current task needs, in a signed section saying for what.
4. Mask account numbers and IDs in the card (`…1234`).

## Look something up

1. Search notes with `type: document` in every scope (summary, contains, tags). Then search the `.txt` copies if needed.
2. If a card's **Contains** covers the question but **Extracted** doesn't: reopen the original, extract, and append a new signed section to the card.
3. For **money, legal or health** questions, always reopen the original. Never answer from extracts alone.
4. Answer citing the card: `[[<card>]]`.

## Existing archives (years of files)

Don't catalog everything at once.

- **On demand:** create a card the first time a document is used.
- **Light pass, per folder, when asked:** cards with just filename, date, type and a one-line summary. Show the person a dry-run list first.
- Keep a note (`type: note`, in `personal/records/`) listing which folders have been cataloged, and when.

## Never

- Delete, rename or edit originals.
- Copy originals into the vault.
- Put documents or card contents in notifications, messages or anything outside the vault.
