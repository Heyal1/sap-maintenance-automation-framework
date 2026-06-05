# Architecture

This framework runs SAP maintenance through Azure DevOps pipelines that call
Ansible playbooks on a dedicated runner. The public repository contains a small
synthetic inventory so adopters can understand the shape of the automation
without exposing private systems.

## Pipeline Flow

1. `00-sap-host-info-pipeline.yml` scans selected hosts and produces a report.
2. `01-staging-pipeline.yml` stages SAP media from a local source or SAP
   Download Basket.
3. `02-maintenance-pipeline.yml` runs the maintenance workflow:
   PreCheck, IcingaDowntime, StopApplications, KernelUpdate, HanaUpdate,
   HanaMiniChecks, OsPatch, StartApplications, ValidationNotify, and
   FailureNotify.

## Playbook Flow

- `01_sap_host_info.yml` discovers SAP and HANA versions.
- `02_staging.yml` prepares and distributes SAP media.
- `03_maintenance_precheck.yml` validates inventory, credentials, versions, and
  Icinga health.
- `03_maintenance_downtime.yml` sets or records Icinga downtime handling.
- `03_maintenance_stop.yml` stops SAP application and HANA services.
- `03_maintenance_kernel.yml` updates SAP kernel files and handles rollback.
- `03_maintenance_hana.yml` updates dedicated HANA systems and shared HANA
  instances.
- `03_maintenance_os.yml` patches the operating system.
- `03_maintenance_start.yml` starts SAP application and HANA services.
- `03_maintenance_validation.yml` validates health and renders reports.

## State Files

Maintenance stages exchange state on the Ansible controller under
`controller_state_base` from `vars/common.yml`. State files hold timestamps,
version snapshots, update results, and report inputs. They are runtime data and
must not be committed.

## Shared HANA Flow

Shared HANA hosts are modeled under `SHARED_HANA`. Each physical HANA host has
`hana_instances`; each instance has tenants with a `customer`, `update_tier`,
`app_hosts`, and optional Icinga services. Validation requires every tenant
customer to be a real top-level inventory group and every app host to exist in
inventory with a matching primary `sap_sid`.
