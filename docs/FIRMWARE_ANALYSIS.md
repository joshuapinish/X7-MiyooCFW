# Original firmware analysis

## Known artifact families

The prior extraction contains decoded payloads and original files associated with applications and drivers, including:

- Applications: `home.axf`, `init.axf`, `game_gba.axf`, `game_gbx.axf`, `game_md.axf`, `game_sfc.axf`, `game_nes.axf`, and multiple `game_kg_*.axf` files.
- Drivers: `display.drv`, `audio.drv`, `key.drv`, and `usb_host0.drv`.
- Configuration/resources: `app_config.fex`, `app_config.bin`, `.desktop` entries, `.reg` files, bitmaps, language files and related modules.
- Decoded artifacts use paths such as `apps__home.axf.payload.bin` and `drv__display.drv.payload.bin` in the extraction reports.

This list is an inventory of names, not a claim that each payload has been completely reversed or that every `.axf` is a standard Linux executable.

## Confirmed details from prior analysis

- Prior local analysis identified `drv/display.drv` as a 32-bit little-endian ARM ELF, EABI4, statically linked and stripped. This result must be repeated with `readelf -h -A` because public reverse-engineering references for related ATJ227x systems describe MIPS 4KEc/µC/OS-II. Treat ISA/runtime identification as unresolved until original files and chip marking agree.
- The display driver contains the string `LCD_HSD045F8W7_9806E__4_5` and LCD-related strings such as `lcd0_para`, `lcd_bl_en_used`, `lcd_pwm_used`, `lcdclk`, `lcdde`, `lcdhsync`, and `lcdvsync`.
- The extracted `app_config.fex` contains sections named `[lcd_para]` and `[display_para]`.
- The PC-visible game volume has `GAME/{FC,GB,GBC,GBA,MD,SFC,MAME}` and a `GAME_MEMORY` directory.
- `GAME_MEMORY00.KG` is 32 bytes and contains the ASCII path `f:\\Juegos\\supersonics1_beta4.bin`. This indicates a path/reference field, but the format and purpose of every `.KG` file are not yet known.

## Mandatory architecture verification

Re-run `file` and `readelf -h -A` on the original, not merely decoded, versions of `drv/display.drv`, `apps/home.axf`, `apps/init.axf`, and at least one game emulator. Save the exact `Machine:`, ELF flags and ABI attributes, plus SHA-256. If the results differ between files, identify which runtime/processor each targets. Track this as a blocker in [ISA/runtime discrepancy](ISA_RUNTIME_DISCREPANCY.md).

## Next analysis tasks

1. Generate SHA-256 manifest and size inventory for extracted firmware artifacts.
2. Run `file`, `readelf -h -l -S -A`, and architecture-aware disassembly on each executable; distinguish valid ELF files from extracted payloads that require wrapper removal.
3. Compare strings and references between menu/launcher programs and emulator binaries to trace game launch commands and expected file formats.
4. Inspect representative `.KG` game files using header signatures and entropy/compression checks. Do not describe them as encrypted or as a known archive format until signatures or a parser confirm it.
5. Trace all LCD-related data references and reconstruct the actual initialization table and bus writes.
6. Inspect button, audio, SD/storage and USB-related binaries and configuration sections.
7. Keep copyrighted ROMs, vendor firmware blobs, keys, and full-card images out of public repository commits unless distribution is explicitly permitted.

## Reporting standard

For every finding record: source file, original and extracted paths, SHA-256, offset, command/tool version, output, confidence, and the next test that could disprove the hypothesis.
