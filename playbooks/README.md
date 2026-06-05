# Playbooks

The playbooks contain the Ansible orchestration for discovery, staging,
maintenance, validation, and reporting.

## Core Playbooks

| Playbook | Purpose |
| --- | --- |
| `01_sap_host_info.yml` | Discover SAP instances and generate host info reports |
| `02_staging.yml` | Prepare and distribute SAP media |
| `03_maintenance_precheck.yml` | Validate inventory, versions, credentials, and Icinga health |
| `03_maintenance_downtime.yml` | Set or record Icinga downtime handling |
| `03_maintenance_stop.yml` | Stop SAP and HANA services |
| `03_maintenance_kernel.yml` | Update SAP kernel files and rollback on failure |
| `03_maintenance_hana.yml` | Update dedicated and shared HANA systems |
| `03_maintenance_os.yml` | Patch the operating system |
| `03_maintenance_start.yml` | Start SAP and HANA services |
| `03_maintenance_validation.yml` | Validate health, compare versions, and render reports |
| `03_maintenance_cleanup.yml` | Manual cleanup for retained downtime state |

## Shared Tasks

Shared tasks under `playbooks/tasks/` handle SAP discovery, inventory
validation, Icinga target derivation, HANA prechecks, shared HANA instance
context building, state loading, version comparison, and error notification.

## State Model

Maintenance stages exchange state through files on the Ansible controller:

```text
<controller_state_base>/<customer>/<environment>/<run_id>/
  start.txt
  end.txt
  <sid>/
    ver_before_<host>.txt
    hana_ver_before_<host>.txt
    kernel_state_<host>.json
    os_state_<host>.json
    hana_state_<host>.json
```

These files are runtime artifacts and must not be committed.

## HANA Credential Pattern

HANA credentials are read from environment variables using:

```text
<CUSTOMER>-HANA-<SID>-<ROLE>
```

The playbooks also check underscore variants because shell environment
variables commonly use underscores.
