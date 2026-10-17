# Research references

This file lists public sources and records how each should be used. Upstream documentation describes its own supported devices; it does not verify our exact board.

## Primary project and compatibility references

- [MiyooCFW upstream repository](https://github.com/TriForceX/MiyooCFW) — authoritative source for the firmware codebase and releases.
- [MiyooCFW wiki: compatible consoles and notes](https://github.com/TriForceX/MiyooCFW/wiki/) — says supported hardware uses Allwinner F1C100S or F1C500S; lists Powkiddy X7 as not confirmed. This does not establish compatibility with the X7 MP5 investigated here.
- [MiyooCFW releases](https://github.com/TriForceX/MiyooCFW/releases) — reference builds and installation assumptions for supported devices. Do not flash these images to this target.
- [ATJ227X firmware tools by mcirsta](https://github.com/mcirsta/ATJ227X_firmware_tools) — public tooling for unpacking/working with Actions ATJ227X (including ATS3603). Use as a format-analysis reference, not proof of the exact chip in any particular console.

## Actions ATJ227x CPU/runtime references

- [ATJ227x reverse-engineering notes by pulkomandy](https://pulkomandy.tk/_/_Electronique/_Reverse%20Engineering%20notes%20for%20ATJ227x) — first-hand analysis of related ATJ2279B devices; describes µC/OS-II, ELF apps and a MIPS toolchain. This is related-platform evidence, not proof of the exact SoC in the X7 MP5.
- [ActSDK by mcirsta](https://github.com/mcirsta/ActSDK) — SDK identified as targeting Actions SoCs running µC/OS; its application Makefile explicitly says “MIPS 4KEc (32 bit RISC) - Actions board”. Again, confirm applicability to the user's exact revision.
- [ATJ227X family datasheet PDF](https://pulkomandy.tk/ATJ227x/Datasheets/ATJ227X_Datasheet_V1.0_101126.pdf) — family-level hardware reference; verify the exact chip revision and treat secondary summaries cautiously.
- [ATJ2273B secondary datasheet summary](https://www.datasheetcafe.com/atj2273b-pdf-datasheet-24428/) — internally contains conflicting CPU descriptions, so it is not sufficient to settle ISA.

These sources conflict with the earlier local report that `drv/display.drv` is ARM ELF. The conflict is explicitly tracked in [ISA/runtime discrepancy](../docs/ISA_RUNTIME_DISCREPANCY.md).

## Local project evidence

- Prior extraction workspace: `~/X7-FirmwareLab`.
- Recorded full SD image: `/home/joshua/sd-backup-completo.img` (reported size 7,988,051,968 bytes); verification details remain to be documented.
- Original display-driver identifiers and `app_config.fex` sections are summarized in [Firmware analysis](../docs/FIRMWARE_ANALYSIS.md) and [Hardware inventory](../docs/HARDWARE.md).

## Evidence discipline

For each additional external source, record publisher, URL, access date, applicable chip/board revision, and the exact claim it supports. Distinguish public documentation from forum reports and from findings measured on the user's own device.
