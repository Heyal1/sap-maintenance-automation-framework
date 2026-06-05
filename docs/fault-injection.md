# Fault Injection

This project exposes stage-specific fault injection switches so the maintenance rescue paths can be tested without waiting for a real platform failure.

## Rules

- Use literal YAML/JSON booleans: `true` and `false`.
- Do not use `yes` or `no`.
- Enable one fault injection switch at a time.
- These switches are intended for deliberate manual validation via `--extra-vars`.
- Do not add them as Azure DevOps pipeline parameters.

## Available Switches

- `inject_failure_precheck`
- `inject_failure_stop`
- `inject_failure_kernel`
- `inject_failure_hana`
- `inject_failure_os`
- `inject_failure_start`
- `inject_failure_validation`

## Activation Examples

Run PreCheck fault injection:

```bash
ansible-playbook playbooks/03_maintenance_precheck.yml \
  -i inventory/inventory.yml \
  --extra-vars '{"inject_failure_precheck": true, "email_recipient": "none"}'
```

Run StopApplications fault injection. At least one maintenance scope switch must be `true` or the playbook exits as precheck-only:

```bash
ansible-playbook playbooks/03_maintenance_stop.yml \
  -i inventory/inventory.yml \
  --extra-vars '{"do_kernel": true, "inject_failure_stop": true, "email_recipient": "none"}'
```

Run KernelUpdate fault injection. This deliberately exercises the rollback path after the backup step, so use a non-production test target:

```bash
ansible-playbook playbooks/03_maintenance_kernel.yml \
  -i inventory/inventory.yml \
  --extra-vars '{"inject_failure_kernel": true, "email_recipient": "none"}'
```

Run HANAUpdate fault injection:

```bash
ansible-playbook playbooks/03_maintenance_hana.yml \
  -i inventory/inventory.yml \
  --extra-vars '{"inject_failure_hana": true, "email_recipient": "none"}'
```

Run OSPatch fault injection:

```bash
ansible-playbook playbooks/03_maintenance_os.yml \
  -i inventory/inventory.yml \
  --extra-vars '{"inject_failure_os": true, "email_recipient": "none"}'
```

Run StartApplications fault injection. At least one maintenance scope switch must be `true` or the playbook exits as precheck-only:

```bash
ansible-playbook playbooks/03_maintenance_start.yml \
  -i inventory/inventory.yml \
  --extra-vars '{"do_kernel": true, "inject_failure_start": true, "email_recipient": "none"}'
```

Run ValidationNotify fault injection:

```bash
ansible-playbook playbooks/03_maintenance_validation.yml \
  -i inventory/inventory.yml \
  --extra-vars '{"inject_failure_validation": true, "email_recipient": "none"}'
```

## Expected Result

When a fault injection switch is `true`, the target playbook fails deliberately inside its stage workflow and routes through the stage rescue path. That path captures the failing task, renders the stage-specific error context, and triggers the standard failure notification flow.
