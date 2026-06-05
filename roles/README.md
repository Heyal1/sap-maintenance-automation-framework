# Roles

Local roles used by the playbooks.

| Role | Purpose |
| --- | --- |
| `downloadbasket_custom` | Download SAP files from SAP Download Basket |
| `icinga_service_check` | Query Icinga services for critical states |
| `icinga_service_gate` | Poll Icinga until services are healthy or timeout is reached |
| `icinga_downtime` | Set or remove Icinga host downtimes |
| `os_update` | Patch OS packages and optionally reboot |
| `send_email` | Send HTML reports through local sendmail |

The roles are intentionally small. SAP-specific orchestration remains in the
playbooks, while upstream SAP modules and roles remain in the vendored
`sap.sap_operations` collection.
