# FAQ

## Does the repository contain real SAP hosts?

No. `inventory/inventory.yml` is synthetic and uses documentation-only IP
addresses from `192.0.2.0/24`.

## Which systems are demonstrated?

The demo covers a normal SAP environment (`DEMO_DEV`), a dedicated HANA host for
SID `D01`, and a shared HANA host with tenants `A1D`, `B1Q`, and `C1P`.

## Where do credentials come from?

From the Azure DevOps variable group `SAP-Maintenance-Demo-Secrets` or a
company-specific equivalent. HANA secrets follow:

```text
<CUSTOMER>-HANA-<SID>-<ROLE>
```

Example roles are `SIDADM`, `SAPADM`, `SYSTEM`, `ROOT`, and `HANA_ADMIN`.

## Does the repository include SAP software?

No. SAP media must be staged by the adopter through local controller paths or
SAP Download Basket credentials.

## What does Icinga do in the workflow?

The maintenance workflow can set host downtime, run pre-check health gates, poll
post-maintenance health, and keep downtime active when validation fails.

## Can I run only one update type?

Yes. The maintenance pipeline exposes `do_kernel_update`, `do_os_update`, and
`do_hana_update`. Any combination can be selected.

## How are shared HANA tenants modeled?

The shared HANA host is under `SHARED_HANA`. Each tenant references a top-level
inventory customer group and lists application hosts. Validation checks that
each listed app host exists and has the matching primary `sap_sid`.

## Why is `local_collections/` committed?

It pins the SAP operations collection used by the playbooks. Treat it as
vendored upstream code and keep the license files intact.
