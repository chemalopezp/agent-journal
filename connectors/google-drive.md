# Google Drive (document originals)

- **Access:** `drive-setup` installs rclone and the 1Password CLI and fetches a service-account key; the account has Viewer access to the folders the human shares with it. Remote name `pdrive:`, scope `drive.readonly`.
- **Settings (environment variables):** `RCLONE_CONFIG_PDRIVE_TYPE=drive`, `RCLONE_CONFIG_PDRIVE_SCOPE=drive.readonly`, `RCLONE_CONFIG_PDRIVE_SHARED_WITH_ME=true`, `RCLONE_CONFIG_PDRIVE_SERVICE_ACCOUNT_FILE`, `OP_DRIVE_KEY_ITEM`; secret `OP_SERVICE_ACCOUNT_TOKEN`.
- **Use:** list and copy originals to a temporary folder, read, delete the copy. Cards go in the vault (playbooks/documents.md); originals never do.
