# Inventory

`inventory/inventory.yml` contains a compact synthetic scenario for the public
template. It is not a production inventory.

## Demo Groups

```text
DEMO
  DEMO_DEV
    demo-app-01  D01  192.0.2.10
    demo-hdb-01  D01  192.0.2.11

TENANT_A
  TENANT_A_DEV
    tenant-a-app-01  A1D  192.0.2.20

TENANT_B
  TENANT_B_QAS
    tenant-b-app-01  B1Q  192.0.2.21

TENANT_C
  TENANT_C_PRD
    tenant-c-app-01  C1P  192.0.2.22

SHARED_HANA
  SHARED_HANA_demohdb01
    demohdb01  SHARED  192.0.2.30
```

## Host Fields

| Field | Purpose |
| --- | --- |
| `ansible_host` | SSH target address or hostname |
| `sap_sid` | Primary SAP SID on the host; shared HANA uses `SHARED` |
| `sap_sids` | List of all SIDs relevant to the host |
| `hana_shared` | Marks a physical shared HANA host |
| `hana_instances` | Shared HANA instance and tenant metadata |
| `app_hosts` | Application hosts attached to a shared HANA tenant |

## Shared HANA Template

```yaml
SHARED_HANA:
  children:
    SHARED_HANA_demohdb01:
      hosts:
        demohdb01:
          ansible_host: 192.0.2.30
          hana_shared: true
          sap_sid: SHARED
          sap_sids: [A1D, B1Q, C1P]
          hana_instances:
            - instance_nr: "01"
              instance_name: H01
              tenants:
                - sid: A1D
                  customer: TENANT_A
                  update_tier: dev
                  app_hosts: [tenant-a-app-01]
                  icinga_services: []
```

Validation expects:

- Every tenant `customer` is a real top-level inventory group.
- Every tenant SID appears in the shared host `sap_sids` list.
- Every `app_hosts` entry exists in inventory.
- Every app host has a primary `sap_sid` matching the tenant SID.

## Target Limits

Normal target:

```bash
ansible-playbook playbooks/01_sap_host_info.yml -i inventory/inventory.yml -l DEMO_DEV
```

Shared HANA target:

```bash
ansible-playbook playbooks/03_maintenance_hana.yml -i inventory/inventory.yml -l SHARED_HANA_demohdb01
```
