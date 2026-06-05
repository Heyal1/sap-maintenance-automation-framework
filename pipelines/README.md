# Pipelines

Azure DevOps pipeline templates for the SAP Maintenance Automation Framework.
They are manually triggered and expect an Ansible-capable runner.

## Required Adaptation

- Replace the agent pool `SAP Maintenance Runner` with your real pool if
  needed.
- Replace variable group `SAP-Maintenance-Demo-Secrets`.
- Provide Icinga, SAP Download Basket, and HANA secrets.
- Adjust `PROJECT_ROOT` if your Azure DevOps checkout path differs.

## Pipeline 0: SAP Host Info

File: `00-sap-host-info-pipeline.yml`

Scans selected hosts and creates a host information report.

| Parameter | Default | Purpose |
| --- | --- | --- |
| `customer` | `DEMO` | Inventory customer group |
| `environment` | `DEV` | Inventory environment suffix |
| `target_override` | `none` | Optional direct host or group limit |
| `include_kernel_guide` | `true` | Include kernel guide section |
| `include_hana_guide` | `true` | Include HANA guide section |
| `email_recipient` | `none` | Optional report recipient |

## Pipeline 1: Staging

File: `01-staging-pipeline.yml`

Stages SAP media from a local controller directory or SAP Download Basket.

| Parameter | Default | Purpose |
| --- | --- | --- |
| `customer` | `DEMO` | Inventory customer group |
| `environment` | `DEV` | Inventory environment suffix |
| `staging_method` | `local` | `local` or `download_basket` |
| `stage_kernel` | `true` | Stage kernel media |
| `stage_hana` | `true` | Stage HANA media |
| `stage_hostagent` | `true` | Stage SAP Host Agent media |
| `source_directory` | `/home/aktansible/sap_staging/source/` | Local media source |

## Pipeline 2: Maintenance

File: `02-maintenance-pipeline.yml`

Runs the maintenance workflow. Normal groups use `customer_environment` limits
such as `DEMO_DEV`. Shared HANA runs use `customer=SHARED_HANA` and
`environment=SHARED_HANA_demohdb01`.

| Parameter | Default | Purpose |
| --- | --- | --- |
| `customer` | `DEMO` | Demo customer or `SHARED_HANA` |
| `environment` | `DEV` | Demo environment or shared HANA group |
| `do_kernel_update` | `true` | Run SAP kernel update |
| `do_os_update` | `false` | Run OS patching |
| `do_hana_update` | `false` | Run HANA update |
| `skip_icinga` | `false` | Bypass Icinga API actions |
| `email_recipient` | `none` | Optional report recipient |

## Secret Names

Demo variable group: `SAP-Maintenance-Demo-Secrets`.

| Secret | Purpose |
| --- | --- |
| `ICINGA-URL` | Icinga API URL |
| `ICINGA-USER` | Icinga API user |
| `ICINGA-PASS` | Icinga API password |
| `SAP-SUPPORT-USER` | SAP Download Basket user |
| `SAP-SUPPORT-PASSWORD` | SAP Download Basket password |
| `HANA-ADMIN-USER` | Optional HANA admin username |
| `<CUSTOMER>-HANA-<SID>-<ROLE>` | HANA passwords |

HANA roles used by the playbooks: `SIDADM`, `SAPADM`, `SYSTEM`, `ROOT`, and
`HANA_ADMIN`.
