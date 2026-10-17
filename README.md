# X7-MiyooCFW

Experimental research and hardware bring-up for an alternative firmware project targeting X7 / MP5 handheld revisions.

**Status: research and bring-up only. This repository does not currently provide a bootable or flashable firmware image.**

## Objective

Investigate whether MiyooCFW components or a compatible Linux-based firmware can be adapted to the X7 MP5. The project does not assume that all devices branded X7 share the same hardware, or that a device can run Linux merely because some firmware binaries are ARM executables.

## Start here

- [Development roadmap](ROADMAP.md)
- [First read-only fire-test campaign](docs/FIRETESTS.md)
- [MiyooCFW architecture and port implications](docs/MIYOO_ARCHITECTURE.md)
- [ISA/runtime discrepancy: mandatory verification](docs/ISA_RUNTIME_DISCREPANCY.md)
- [Hardware findings](docs/HARDWARE.md)
- [Compatibility assessment](docs/COMPATIBILITY.md)
- [Boot-process investigation](docs/BOOT_PROCESS.md)
- [Original firmware analysis](docs/FIRMWARE_ANALYSIS.md)
- [Linux feasibility decision](docs/LINUX_FEASIBILITY.md)
- [Research references](research/REFERENCES.md)

## Current evidence snapshot

- The original firmware has been extracted for analysis; relevant decoded artifacts include application payloads such as `apps__home.axf.payload.bin`, `apps__init.axf.payload.bin`, `apps__game_gba.axf.payload.bin`, `apps__game_sfc.axf.payload.bin`, `apps__game_md.axf.payload.bin`, and the `drv__display.drv.payload.bin` / `drv__audio.drv.payload.bin` payloads.
- The original `drv/display.drv` has been identified as a 32-bit little-endian ARM ELF, EABI version 4, statically linked and stripped.
- The display-driver strings include `LCD_HSD045F8W7_9806E__4_5`. The exact panel timings, wiring, reset sequence, pixel format, and effective display mode still require confirmation.
- A full SD image was previously recorded at `/home/joshua/sd-backup-completo.img` with a size of 7,988,051,968 bytes. Checksum and end-to-end verification status must be recorded before treating it as a verified recovery image.
- A PC-accessible FAT volume was observed at `/run/media/joshua/3EDF-BD13` with `GAME/` and `GAME_MEMORY/` directories. The block-device identity and relationship to the console's boot medium are not yet proven.

These observations do **not** establish the exact SoC revision, available RAM, boot ROM behavior, bootloader, kernel, or ability to boot Linux.

## Important compatibility warning

Upstream MiyooCFW documents support for Allwinner F1C100S/F1C500S devices, with some display and hardware revisions needing extra work. Its wiki lists the Powkiddy X7 as unconfirmed; that listing does not prove compatibility with this project's X7 MP5. The target under investigation is the Actions Semiconductor ATJ227x family (candidate ATJ2273B / ATJ2273S); the precise chip marking and board revision must be verified.

A MiyooCFW disk image must not be written to the X7. Reusing portable applications or a frontend may be possible, but a full firmware port requires a compatible boot chain, kernel or equivalent platform layer, and working drivers.

## Host build

The current CMake project validates a portable display-core interface only:

```sh
cmake -S . -B build -DX7_BUILD_TESTS=ON
cmake --build build
ctest --test-dir build --output-on-failure
```

Passing these tests does not initialize the physical LCD and does not produce bootable firmware.

## Safety

- Do not write to a block device until its identity is confirmed.
- Preserve the original image and compute a cryptographic hash; keep a second copy on another physical device.
- Do not flash an image just because its filename contains “X7”.
- Do not attempt bootloader, partition-table, or firmware writes until recovery is documented and independently tested.
- Do not publish commercial ROMs, complete vendor firmware images, or proprietary binaries without redistribution permission.
- Clearly label every feature as confirmed, experimental, or unknown.
