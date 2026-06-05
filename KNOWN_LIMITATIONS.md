# Known Limitations

This repository is a product template. The demo inventory is synthetic and
uses documentation-only addresses from `192.0.2.0/24`.

## Scope

- HANA is the only database update path covered by this template.
- The vendored `sap.sap_operations` collection is treated as upstream code and
  is not refactored in this repository.
- SAP media must be staged with valid SAP files. The repository does not ship
  SAP software.
- The Azure DevOps pipelines are templates. Agent pool names, variable groups,
  secret stores, and network access must be adapted before productive use.

## Operational Gaps To Validate

- End-to-end behavior in each company environment, including rollback and
  failure notification paths.
- Icinga downtime and health gate filters for the target monitoring model.
- Shared HANA sequencing for all tenant tiers and app-host relationships.
- Disk capacity checks and maintenance windows for large HANA systems.
- Local sendmail or relay configuration for report delivery.

## Future Work

- Add a company-specific adoption checklist per environment.
- Add automated tests for shared HANA inventory validation.
- Add a sample private inventory overlay pattern.
- Consider publishing the vendored SAP collection as a pinned artifact instead
  of committing it directly, if license and supply-chain requirements allow it.
