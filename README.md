# SAP Maintenance Automation Framework

Reusable Ansible and Azure DevOps template for SAP maintenance automation.

The framework covers host discovery, SAP media staging, OS patching, SAP kernel
updates, dedicated HANA updates, shared HANA updates, Icinga downtime and health
gates, error notification, and HTML reports.

## Demo Scenario

The public inventory is synthetic. It demonstrates the supported paths without
exposing real customer data:

- `DEMO_DEV`: normal SAP application host plus dedicated HANA host for SID
  `D01`.
- `TENANT_A_DEV`, `TENANT_B_QAS`, `TENANT_C_PRD`: tenant application hosts for
  shared HANA examples.
- `SHARED_HANA_demohdb01`: shared HANA host `demohdb01` with instances `H01`
  and `H02`, tenant/app-host relationships, and validation-ready metadata.

## Workflow

```text
Host Info -> Staging -> Maintenance -> Reports
```

The maintenance pipeline can run SAP kernel, HANA, and OS updates in any
selected combination. HANA paths include dedicated-host updates and shared-host
tenant sequencing.

## Repository Map

| Path | Purpose |
| --- | --- |
| `inventory/` | Synthetic demo inventory and inventory model docs |
| `pipelines/` | Azure DevOps pipeline templates |
| `playbooks/` | Ansible orchestration playbooks and shared tasks |
| `roles/` | Local roles for Icinga, OS update, staging, and email |
| `vars/` | Shared runtime configuration |
| `templates/` | Report and error-notification templates |
| `scripts/` | Helper scripts |
| `local_collections/` | Vendored upstream `sap.sap_operations` collection |
| `docs/architecture.md` | Pipeline, playbook, state, and shared HANA flow |
| `ADOPTION.md` | What a real company must change before use |
| `SECURITY.md` | Secret, inventory, log, and report handling |
| `KNOWN_LIMITATIONS.md` | Current template limitations and future work |

## Local Validation

```bash
ansible-inventory -i inventory/inventory.yml --list
ansible-playbook --syntax-check -i inventory/inventory.yml playbooks/01_sap_host_info.yml
ansible-playbook --syntax-check -i inventory/inventory.yml playbooks/02_staging.yml
ansible-playbook --syntax-check -i inventory/inventory.yml playbooks/03_maintenance_precheck.yml
```

Run the remaining `playbooks/03_maintenance_*.yml` syntax checks before
adopting the template.

## Production Adoption

This repository is not ready for production by cloning alone. Replace the demo
inventory, Azure DevOps variable group, agent pool, monitoring URL, email
settings, SAP media paths, secrets, and network access for your environment.
Use `ADOPTION.md` and `SECURITY.md` as the rollout checklist.
