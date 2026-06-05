# Send Email Role

Sends HTML email through local `sendmail` on the Ansible controller.

## Variables

| Variable | Default | Description |
| --- | --- | --- |
| `email_recipient` | required | Recipient address |
| `email_subject` | `SAP Automation Report` | Subject line |
| `email_html_file` | required | HTML body file |
| `email_sender` | `sap.automation@example.invalid` | Sender address |
| `email_attachment_files` | `[]` | Optional attachment list |

Configure the actual sender address and mail relay outside the public template.
