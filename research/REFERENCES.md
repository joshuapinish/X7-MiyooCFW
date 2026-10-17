# Research references

This file lists public sources and records how each should be used. Upstream documentation describes its own supported devices; it does not verify our exact board.

## Primary project and compatibility references

- [MiyooCFW upstream repository](https://github.com/TriForceX/MiyooCFW) — authoritative source for the firmware codebase and releases.
- [MiyooCFW wiki: compatible consoles and notes](https://github.com/TriForceX/MiyooCFW/wiki/) — says supported hardware uses Allwinner F1C100S or F1C500S; lists Powkiddy X7 as not confirmed. This does not establish compatibility with the X7 MP5 investigated here.
- [MiyooCFW releases](https://github.com/TriForceX/MiyooCFW/releases) — reference builds and installation assumptions for supported devices. Do not flash these images to this target.
- [ATJ227X firmware tools by mcirsta](https://github.com/mcirsta/ATJ227X_firmware_tools) — public tooling for unpacking/working with Actions ATJ227X (including ATS3603). Use as a format-analysis reference, not proof of the exact chip in any particular console.

## Local project evidence

- Prior extraction workspace: `~/X7-FirmwareLab`.
- Recorded full SD image: `/home/joshua/sd-backup-completo.img` (reported size 7,988,051,968 bytes); verification details remain to be documented.
- Original display-driver identifiers and `app_config.fex` sections are summarized in [Firmware analysis](../docs/FIRMWARE_ANALYSIS.md) and [Hardware inventory](../docs/HARDWARE.md).

## Evidence discipline

For each additional external source, record publisher, URL, access date, applicable chip/board revision, and the exact claim it supports. Distinguish public documentation from forum reports and from findings measured on the user's own device.
