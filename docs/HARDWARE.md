# Hardware inventory

**Status:** Partial inventory. Do not treat candidate components as confirmed for all X7/MP5 revisions.

## Known observations

| Item | Observation | Confidence / next verification |
|---|---|---|
| Product label | X7 / MP5 handheld | Product names may cover multiple board revisions. |
| SoC family | Actions Semiconductor ATJ227x is the current project target; ATJ2273B and ATJ2273S are candidate variants | Verify the physical chip marking or an unambiguous hardware identifier. Do not infer from the enclosure name. |
| LCD identifier | Original display-driver string: `LCD_HSD045F8W7_9806E__4_5` | String found in the original driver; does not by itself prove every panel timing or board wiring. |
| LCD/controller | ILI9806E-family controller is under investigation | Confirm from initialization sequence and panel documentation. |
| Display mode | Prior notes mention 854 × 460; panel references for a similarly marked panel mention 480 × 854 | Discrepancy is unresolved. Confirm active resolution, orientation, timings, and usable pixel dimensions from hardware and original config. |
| Original display driver | Prior local analysis reported `drv/display.drv` as 32-bit little-endian ARM ELF/EABI4 | Must be re-verified with `readelf -h -A`: public references for related ATJ227x platforms describe MIPS 4KEc and µC/OS-II. Exact chip and binary provenance are unresolved. |
| Original system runtime | Applications/drivers include `.axf`, `.drv`, `.mod`, and `.plg` artifacts | The precise OS/RTOS and execution environment have not been established from extensions alone. |
| RAM | Unknown for the exact board revision | Measure or recover memory configuration; do not assume 32, 64, 128, or 256 MiB from a model name. |
| Boot chain | Unknown | Identify boot ROM, loader, firmware update path, and recovery mode before attempting a system image. |
| Audio | Original firmware contains `audio.drv` and audio-related modules | Determine output codec/DAC path, amplifier, sample rate, buffer API, and speaker wiring. |
| Controls | Original firmware contains key/input driver artifacts including `key.drv` and `key_REF.dat` | Map button codes and scan mechanism from configuration/driver analysis and safe runtime tests. |
| PC-accessible storage | A FAT volume was seen mounted at `/run/media/joshua/3EDF-BD13`, reported as 6.8 GiB, with `GAME/` and `GAME_MEMORY/` | It is not yet proven whether this is removable game storage, internal storage exposed by USB, or the boot medium. |
| Backup image | `/home/joshua/sd-backup-completo.img`, 7,988,051,968 bytes according to prior notes | Hash and end-to-end verification still must be recorded explicitly. |

## Critical unresolved ISA/runtime discrepancy

Prior local analysis reported the original display driver as ARM ELF, while public reverse-engineering notes and ActSDK for related Actions ATJ227x systems point to MIPS 4KEc and µC/OS-II. Do not treat the candidate ATJ2273B/ATJ2273S identity or the runtime as confirmed until the physical chip marking and the ELF Machine field of the original apps/drivers have been checked. See [ISA/runtime discrepancy](ISA_RUNTIME_DISCREPANCY.md).

## Evidence to collect

- Board photographs with the SoC and memory markings legible.
- Model/PCB revision, date codes, and connector labels.
- Read-only block-device inventory: model, serial (keep private if publishing), size, partition table, filesystem, UUID, and mount source.
- Original firmware hashes and an artifact manifest.
- Relevant `app_config.fex` display/pin sections; driver strings and disassembly offsets.
- Button mapping, LCD init table, bus type, reset polarity, backlight PWM/GPIO, audio route, and power/sleep behavior.

## Evidence labels

Use **confirmed** only when supported by a direct observation or reproducible analysis. Use **candidate** for a plausible identification and **unknown** when no reliable evidence is available. Keep device-specific serial numbers and user-specific paths out of public reports.
