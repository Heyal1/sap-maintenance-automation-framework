# Icinga Service Check Role

Queries Icinga for critical or unknown services on a target host.

## Variables

| Variable | Default | Description |
| --- | --- | --- |
| `icinga_url` | `https://icinga.example.invalid:5665` | Icinga REST API URL |
| `icinga_user` | `""` | Icinga API username |
| `icinga_password` | `""` | Icinga API password |
| `target_hostname` | `{{ inventory_hostname }}` | Icinga host name |
| `target_host_address` | `{{ ansible_host }}` | Icinga host address |
| `exclude_services` | `['uptime']` | Exact service-name exclusions |
| `exclude_service_prefixes` | `[]` | Prefix exclusions |

The role sets `icinga_critical_services` with the remaining critical or unknown
services after filtering.
