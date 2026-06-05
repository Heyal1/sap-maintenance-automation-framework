# Icinga Downtime Role

Manages Icinga downtimes through the REST API.

## Variables

| Variable | Default | Description |
| --- | --- | --- |
| `icinga_url` | `https://icinga.example.invalid:5665` | Icinga REST API URL |
| `icinga_user` | `""` | Icinga API username |
| `icinga_password` | `""` | Icinga API password |
| `icinga_action` | `set` | `set` or `remove` |
| `icinga_duration` | `3600` | Downtime duration in seconds |
| `icinga_comment` | `SAP Maintenance via Ansible Automation` | Downtime comment |

Set `ICINGA_URL`, `ICINGA_USER`, and `ICINGA_PASS` through the pipeline secret
store for real environments.
