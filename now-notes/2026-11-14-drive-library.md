# Drive library audited every run

Status: config/drive-map.json declares the Heartside root in drive_map (drive-map/1); engine/drive_library.py audits the library Control Center serves in the directive (protocol 1.35.0) with drive_audit.audit on every run, counts only, unknown never clean. Served once Control Center's DRIVE_LIBRARY_PART flag is on.
Next: after Control Center's first complete Drive read, confirm a run's summary shows drive.state checked.
North Star check (2026-11-14): holds.
