# Adapter: ChatGPT + Google Drive (no hosting)

For people who use ChatGPT on their phone. Storage is a Google Drive folder. Works on Plus.

**Limits:** saving is manual (a paste step), and signatures/append-only depend on the human. Test each piece before relying on it.

## Setup

1. **Drive:** create a `Context` folder with the `skills/journal/starter/` structure. Google Docs are easier to edit on a phone than `.md`; either works if the connector can read them.
2. **ChatGPT:** enable the Google Drive connector. Turn **Memory on** (it's the only layer present in every chat; keep it to key facts).
3. **Custom Instructions** (Settings → Personalization):

   > My personal context is in Google Drive, folder "Context". For anything about my life, plans, people or tasks, search that folder first, starting with "About me" and "Inbox". Don't guess facts about me; ask. When I share something worth keeping, end with a "📌 Save" block: date, one line, which note it goes in. Don't bring up sensitive details unless I do.

4. **Tasks** (scheduled, they notify in ChatGPT):
   - **07:00 daily:** "Morning digest. Read my Drive 'Context' folder (Inbox, active projects, last journal entries). Give me today's top 3, people to follow up with, and anything pending. Max 8 lines."
   - **19:00 daily:** "Evening check-in. Ask me 3 short questions about my day, then turn my answers into a 📌 Save block for my journal."

## Test first

Run the morning Task once. If it shows things from the Drive notes, it works. If not, Tasks can't reach Drive: change the morning prompt to "ask me my top 3 for today" and continue in that chat, where Drive does work.

## Saving

Paste "📌 Save" blocks into `00-inbox` (or say "remember this" for key facts). An agent with full access can file them later following `AGENTS.md`.
