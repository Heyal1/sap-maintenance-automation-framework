# Icinga Service Gate Role

Polls Icinga until services are healthy or the configured timeout is reached.

## Variables

| Variable | Default | Description |
| --- | --- | --- |
| `pause_duration` | `0` | Optional fixed pause before check |
| `gate_poll_mode` | `false` | Enable polling mode |
| `gate_poll_interval` | `120` | Seconds between polls |
| `gate_max_wait_seconds` | `1200` | Maximum polling time |
| `gate_fail_on_critical` | `true` | Fail when critical services remain |
| `icinga_url` | `https://icinga.example.invalid:5665` | Icinga REST API URL |

The role uses `icinga_service_check` for the final service list.
