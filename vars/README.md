# vars

`vars/common.yml` defines shared runtime settings for all playbooks.

## Main Settings

| Variable | Default | Purpose |
| --- | --- | --- |
| `sap_stop_timeout_seconds` | `600` | Max wait for SAP stop |
| `sap_start_timeout_seconds` | `900` | Max wait for SAP start |
| `sap_status_check_retries` | `60` | Stop polling attempts |
| `sap_start_check_retries` | `90` | Start polling attempts |
| `icinga_author_prefix` | `Ansible_Automation` | Downtime author prefix |
| `icinga_post_validation_pause_seconds` | `600` | Stabilization pause before health gate |
| `controller_staging_base` | `/home/aktansible/sap_staging` | Controller SAP media staging base |
| `controller_state_base` | `/home/aktansible/tmp` | Cross-stage state base |
| `remote_staging_dir` | `/usr/sap/tmp/staging` | Remote SAP staging base |
| `state_retention_days` | `30` | Runtime state retention |
| `email_default_recipient` | `sap-operations@example.invalid` | Fallback recipient |
| `email_sender` | `sap.automation@example.invalid` | Report sender |

## Usage

Pipelines pass the file with `-e @vars/common.yml`:

```bash
ansible-playbook playbooks/03_maintenance_precheck.yml \
  -i inventory/inventory.yml \
  -l DEMO_DEV \
  -e @vars/common.yml
```

Override values per run with later `-e` arguments.
