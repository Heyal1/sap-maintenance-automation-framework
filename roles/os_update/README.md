# OS Update Role

Ansible role for OS patching with comprehensive logging and optional reboot.

## Features

- **Package Updates**: Update all packages via dnf/yum
- **Package Exclusions**: Exclude specific packages from updates
- **Automatic Reboot**: Optional system reboot after patching
- **Dry Run Mode**: Simulate updates without making changes
- **Comprehensive Logging**: Detailed logging to control node
- **Version Tracking**: Capture OS/kernel versions before and after

## Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `os_update_dry_run` | `false` | Dry run mode - no actual changes |
| `os_update_reboot` | `true` | Reboot system after patching |
| `os_update_excluded_packages` | `[]` | List of packages to exclude from updates |
| `os_update_log_file` | `/var/log/ansible_patch.log` | Log file path on control node |
| `os_update_reboot_timeout` | `300` | Reboot timeout in seconds |
| `os_update_reboot_connect_timeout` | `5` | Connection timeout after reboot |
| `os_update_reboot_pre_delay` | `0` | Delay before reboot |
| `os_update_reboot_post_delay` | `30` | Delay after reboot |

## Example Usage

### Standard OS Patching with Reboot

```yaml
- name: Update OS packages with reboot
  include_role:
    name: os_update
  vars:
    os_update_reboot: yes
    os_update_excluded_packages:
      - kernel*
      - systemd*
```

### Dry Run (No Changes)

```yaml
- name: Simulate OS patching
  include_role:
    name: os_update
  vars:
    os_update_dry_run: true
    os_update_reboot: true
```

### Update Without Reboot

```yaml
- name: Update packages without reboot
  include_role:
    name: os_update
  vars:
    os_update_reboot: no
```

## Output Variables

The role sets the following facts:

| Variable | Description |
|----------|-------------|
| `os_version_before` | OS version before patching |
| `os_version_after` | OS version after patching |
| `linux_kernel_before` | Kernel version before patching |
| `linux_kernel_after` | Kernel version after patching |
| `patch_count` | Number of packages updated |
| `maintenance_start_time` | ISO8601 timestamp of start |
| `maintenance_end_time` | ISO8601 timestamp of end |

## How It Works

1. **Pre-Patching**: Capture current OS/kernel versions
2. **Check Updates**: List available package updates
3. **Apply Updates**: Install updates (skipped in dry run)
4. **Reboot**: Optionally reboot system
5. **Post-Patching**: Re-gather facts and capture new versions
6. **Logging**: Write all operations to log file on control node

## License

MIT
