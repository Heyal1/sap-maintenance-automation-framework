# Downloadbasket Custom Role

Standalone SAP file download role using a Python script with `requests.Session`. Independent from the upstream `sap.sap_operations.swdc_auth_info` module which had authentication issues (HTTP 410/401).

## How It Works

1. **Get basket contents** - Queries SAP download basket via `sap.sap_operations.me_downloadbasket_info`
2. **Get file metadata** - Retrieves download URLs via `sap.sap_operations.me_file_info`
3. **Download files** - Executes `download_sap_files.py` Python script with `requests.Session`
4. **Set permissions** - Makes SAPCAR executable

The Python script handles SAP SAML authentication and redirects automatically using `requests.Session`, bypassing the broken `swdc_auth_info` module.

## Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `downloadbasket_username` | `$SAP_OPERATIONS_DOWNLOAD_USERNAME` | SAP Support Portal username |
| `downloadbasket_password` | `$SAP_OPERATIONS_DOWNLOAD_PASSWORD` | SAP Support Portal password |
| `downloadbasket_destination` | `""` (required) | Absolute path to download directory |
| `downloadbasket_validate_certs` | `true` | Validate SSL certificates |
| `downloadbasket_timeout` | `3600` | Download timeout in seconds |
| `downloadbasket_mode` | `0755` | File permissions for downloaded files |
| `downloadbasket_download_item_types` | `[]` | Filter by item type (empty = all) |

## Example Usage

```yaml
- name: Download SAP files from basket
  include_role:
    name: downloadbasket_custom
  vars:
    downloadbasket_destination: "/home/aktansible/sap_kernel_update/downloads/kernels"
```

Credentials are read from environment variables by default.

## Files

```
downloadbasket_custom/
├── README.md
├── defaults/main.yml          # Default variables
├── files/download_sap_files.py  # Python download script
├── meta/main.yml              # Role metadata
└── tasks/main.yml             # Task definitions
```

## Python Script

`download_sap_files.py` uses `requests.Session` to:
- Authenticate with SAP Support Portal
- Handle SAML redirects automatically
- Download files with progress tracking
- Retry on transient failures

## Dependencies

- Python 3 with `requests` library (on Ansible controller)
- `sap.sap_operations` collection (for `me_downloadbasket_info` and `me_file_info` modules)
