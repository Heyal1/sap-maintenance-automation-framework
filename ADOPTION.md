# Adoption Guide

Use this checklist before running the template in a real company environment.

## Replace Demo Data

- Replace `inventory/inventory.yml` with private inventory kept outside any
  public repository.
- Keep customer groups, environment groups, `sap_sid`, `sap_sids`, and shared
  HANA tenant metadata consistent with `inventory/README.md`.
- Verify every shared HANA tenant `customer` exists as a top-level group.
- Verify every shared HANA `app_hosts` entry exists and has a matching primary
  `sap_sid`.

## Azure DevOps

- Set the pipeline agent pool to your runner, for example a private Ansible
  controller pool.
- Replace `SAP-Maintenance-Demo-Secrets` with your variable group or secret
  store integration.
- Set `AZURE-DEVOPS-PIPELINE-URL-BASE` if error emails should link to pipeline
  runs.

## Secrets

- Provide Icinga secrets: `ICINGA-URL`, `ICINGA-USER`, `ICINGA-PASS`.
- Provide SAP Download Basket secrets if using `download_basket`:
  `SAP-SUPPORT-USER`, `SAP-SUPPORT-PASSWORD`.
- Provide HANA secrets with `<CUSTOMER>-HANA-<SID>-<ROLE>` naming.
- Set `HANA-ADMIN-USER` if the admin username is not `HANA_ADMIN`.

## Runtime Paths

- Confirm controller staging paths in `vars/common.yml`.
- Confirm remote staging paths on SAP and HANA hosts.
- Confirm state retention and cleanup settings.
- Ensure the Ansible runner can write logs and reports locally.

## Network And Host Access

- Ensure SSH access from the runner to every SAP host.
- Ensure sudo/become policy matches the playbook requirements.
- Ensure Icinga API access from the runner.
- Ensure sendmail or an equivalent mail relay is configured.
- Ensure SAP media paths contain SAPCAR and required SAR archives.

## Validation

Run inventory and syntax checks before any live maintenance run. Then validate
on a non-production system with `skip_icinga=true` only if monitoring credentials
are intentionally unavailable.
