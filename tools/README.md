# Research tools

Scripts in this directory should make analysis reproducible and default to read-only behavior.

## Initial tool priorities

- Device inventory that records device paths, sizes, transports, filesystems and mountpoints without writing to devices.
- Hash and manifest generation for original images and extracted artifacts.
- Firmware container/header inspection and byte-signature reports.
- ELF/AXF inventory using `file`, `readelf`, `strings` and architecture-aware disassembly.
- LCD configuration/driver string extraction.
- ROM-container header analysis that reports signatures without redistributing game data.

## Requirements for new scripts

- Never hard-code a device such as `/dev/sda` as a write target.
- Never write, partition, format, or flash by default.
- Make the analyzed source path explicit and reject missing/ambiguous paths.
- Write reports under a project report directory, never into the source medium.
- Record tool versions, exact commands and SHA-256 hashes where applicable.
- Avoid logging serial numbers, credentials or private host paths into public artifacts.
