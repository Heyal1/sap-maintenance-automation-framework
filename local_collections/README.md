# Local Collections

Lokal gebündelte Upstream-Ansible-Collections für Versionskontrolle und Reproduzierbarkeit.

## Was macht dieser Ordner?

Hier liegt eine unveränderte Kopie der `sap.sap_operations`-Collection (v2.17.0). Die Collection wird im Repository mitgeliefert, um eine definierte, getestete Version sicherzustellen und Offline-Verfügbarkeit zu gewährleisten. Authentifizierungsprobleme der Upstream-`downloadbasket`-Rolle werden durch die eigene Rolle `downloadbasket_custom` (unter `roles/`) umgangen – nicht durch Patches an der Collection selbst.

> **WICHTIG:** Niemals `ansible-galaxy collection install sap.sap_operations` ausführen – das würde die versionsgepinnte Collection mit einer möglicherweise inkompatiblen Upstream-Version überschreiben!

## Genutzte Rollen aus der Collection

- `sap_kernel_update` – SAP-Kernel-Patch mit Backup
- `host_info` – System-Discovery (SID, Instanzen, Datenbanken)
- `system` – Lifecycle-Management (Stop/Start mit Wait)
- `downloadbasket` – SAP-Medien-Download (nur basket info-Module)
- `hana_update` – HANA-Datenbank-Updates

## Lokale Anpassungen

- Die Collection selbst ist **unverändert** gegenüber der Upstream-Version v2.17.0
- Authentifizierungsprobleme der Upstream-`downloadbasket`-Rolle werden durch die separate Rolle `downloadbasket_custom` (unter `roles/`) gelöst

## Konfiguration

`ansible.cfg` ensures local collections take priority:

```ini
[defaults]
collections_path = ./local_collections:~/.ansible/collections:/usr/share/ansible/collections
```


## Nach einem Collection-Update

Falls die Upstream-`sap.sap_operations`-Collection aktualisiert werden soll:
1. Neue Version lokal testen (insbesondere Kompatibilität mit `downloadbasket_custom` und den genutzten Rollen prüfen)
2. Kopie in `local_collections/` ersetzen
3. Staging-Pipeline testen (Download + Extraktion) bevor deployed wird

## Bezug zum Gesamtprojekt

Diese Collection liefert die Kernfunktionalität für SAP-Operationen (Host-Info, Kernel-Update, HANA-Update, System Stop/Start). Ohne sie funktioniert keines der SAP-bezogenen Playbooks.
