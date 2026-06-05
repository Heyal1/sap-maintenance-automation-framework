# Templates

Jinja2 templates for generated reports and error notifications.

| Template | Used By | Purpose |
| --- | --- | --- |
| `sap_host_info_report.j2` | `01_sap_host_info.yml` | Host discovery report |
| `staging_report.j2` | `02_staging.yml` | SAP media staging report |
| `maintenance_report.j2` | `03_maintenance_validation.yml` | Final maintenance report |
| `kernel_env_comparison.j2` | `03_maintenance_validation.yml` | Kernel environment comparison |
| `error_notification.md.j2` | Maintenance rescue tasks | Failure notification markdown |

Markdown output is converted to HTML by `scripts/md_to_html_email.py` and sent
with the `send_email` role when an email recipient is configured.
