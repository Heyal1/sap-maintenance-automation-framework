# Project Overview

This repository is a portfolio-grade product template for SAP maintenance
automation with Ansible and Azure DevOps.

It keeps the existing automation structure focused and reusable:

- Azure DevOps pipelines select targets and update scopes.
- Ansible playbooks orchestrate discovery, staging, maintenance, validation,
  and reporting.
- Local roles handle Icinga, OS patching, SAP media download support, and email.
- The vendored SAP collection remains upstream code and is not refactored.

## Supported Demo Paths

- SAP host information report for `DEMO_DEV`.
- SAP media staging for demo customer/environment groups.
- OS update path.
- SAP kernel update path.
- Dedicated HANA update path on `demo-hdb-01`.
- Shared HANA update path on `demohdb01` with tenant/app-host mappings.
- Icinga downtime and health gate integration.
- Failure notification and final report rendering.

## Design Boundary

The template intentionally avoids customer-specific assumptions. Real adopters
must provide private inventory data, private secrets, runner connectivity, SAP
software media, and monitoring configuration outside the public repository.
