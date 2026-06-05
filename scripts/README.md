# Scripts

Hilfsskripte für die SAP-Automatisierung.

## Was macht dieser Ordner?

Hier liegen Python-Skripte, die von den Playbooks als Hilfswerkzeuge aufgerufen werden.

## Dateien

| Skript | Zweck |
|--------|-------|
| `md_to_html_email.py` | Wandelt Markdown-Dateien in formatierte HTML-E-Mails um |

## md_to_html_email.py

Dieses Skript wird von den Playbooks aufgerufen, nachdem ein Report per Jinja2-Template als Markdown erzeugt wurde. Es konvertiert das Markdown in HTML, damit die E-Mail im Posteingang vernünftig formatiert angezeigt wird.

**Aufruf im Playbook:**
```yaml
- name: Convert report to HTML
  command: python3 {{ playbook_dir }}/../scripts/md_to_html_email.py input.md output.html
```

## Bezug zum Gesamtprojekt

Die Skripte sind Helfer im Reporting-Workflow: `Template (.j2)` → `Markdown (.md)` → `scripts/md_to_html_email.py` → `HTML (.html)` → `send_email`-Rolle → E-Mail an Empfänger.
