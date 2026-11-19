---
type: rules
author: human
---
# My rules for agents

The base (instructions, templates, runs, connectors) comes from agent-journal (https://github.com/chemalopezp/agent-journal). This file holds only what's specific to me, and wins on a conflict. My runs are in `runs/`: a note with `base: Day` turns on the base Day run and holds my changes to it. To change a note template, add a file with the same name under `templates/`.

## About me, in one line
*(Details in [[about]].)*

## My rules
- 

## Settings

```yaml
agent_name: Claude          # how agents sign
timezone: UTC               # your IANA timezone
documents_root:             # where originals live (an rclone remote or a synced folder)
base_version: v0.1.0        # agent-journal version to read the base from
```
