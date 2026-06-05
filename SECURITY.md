# Security

## Secrets

Do not commit secrets to this repository. Use Azure DevOps variable groups or
another managed secret store. The demo secret names are placeholders.

HANA secrets use this pattern:

```text
<CUSTOMER>-HANA-<SID>-<ROLE>
```

Supported roles used by the playbooks include `SIDADM`, `SAPADM`, `SYSTEM`,
`ROOT`, and `HANA_ADMIN`.

## Private Inventory

Real inventories may contain customer names, hostnames, IP ranges, SIDs,
domains, and topology data. Keep them in a private repository or protected
pipeline artifact, not in this public template.

## Logs And Reports

Ansible logs, generated reports, and failure notifications can contain
operational data, hostnames, versions, and error output. The `.gitignore` file
excludes common generated paths, but operators must also avoid publishing logs
from pipeline artifacts.

## Vendored Collection

`local_collections/ansible_collections/sap/sap_operations` is vendored upstream
code. Keep its license files and review upstream changes before replacing it.

## Disclosure

If you find a security issue in this template, report it privately to the
repository owner. Do not include secrets, private hostnames, or customer data in
public issues.
