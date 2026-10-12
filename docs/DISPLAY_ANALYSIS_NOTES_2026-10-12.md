# Display driver findings — 2026-10-12

This report records offsets from the user's local extraction. These offsets are tied to the SHA-256 below and should not be reused for a different firmware revision.

## Input identity

```text
File: extracted/bulk-decoded/drv__display.drv.payload.bin
Size: 214260 bytes (0x344f4)
SHA-256: 35285d204ff342b479385e02fae8718cbd39f3f9727b2a7774facb0c511c63de
Assumed load base: 0xe0300000
```

## Known offsets

| Item | File offset | Candidate virtual address |
|---|---:|---:|
| `lcd0_para` (early occurrence) | `0x002e08` | `0xe0302e08` |
| `SPIWRITE 1` | `0x0039fc` | `0xe03039fc` |
| `SPI_WriteComm = 1` | `0x00591c` | `0xe030591c` |
| Reference containing pointer to `SPI_WriteComm = 1` | `0x007ce4` | `0xe0307ce4` |
| Panel identifier `LCD_HSD045F8W7_9806E__4_5` | `0x016cbc` | `0xe0316cbc` |
| `lcd0_para` (configuration lookup) | `0x021dec` | `0xe0321dec` |
| Reference containing pointer to the second `lcd0_para` | `0x0225b8` | `0xe03225b8` |
| `lcd_bl_en_used` | `0x022134` | `0xe0322134` |
| `lcd_pwm_used` | `0x0221b0` | `0xe03221b0` |
| `lcdclk` | `0x0342d0` | `0xe03342d0` |
| `lcdde` | `0x0342e4` | `0xe03342e4` |
| `lcdhsync` | `0x0342f8` | `0xe03342f8` |
| `lcdvsync` | `0x03430c` | `0xe033430c` |

Virtual addresses assume that the decoded first ELF section is loaded at `0xe0300000`, matching the original ELF entry/segment address. Confirm that mapping before treating these as runtime addresses.

## Current inference

- The string `SPI_WriteComm = 1` is referenced by a literal 32-bit pointer candidate at offset `0x7ce4`. This gives us a useful disassembly window around `0xe0307c90`.
- The later `lcd0_para` occurrence has a pointer candidate near `0x225b8`, in a region that appears to contain configuration/table data. Inspect around `0xe03225a0`.
- There is no literal pointer to the panel identifier at `0xe0316cbc` in the payload. That does not prove it's unused: the address may be formed PC-relatively, through a table, or the string may be logging metadata.
- These matches are leads, not confirmed call graphs. The disassembly wrapper treats the raw payload as one text section, so strings and literal pools may also be printed as bogus ARM instructions.

## Next targeted inspection

From `~/X7-FirmwareLab/X7-MiyooCFW-test` after updating the branch:

```sh
bash scripts/inspect-arm-window.sh \
  build/driver-analysis-decoded/arm-payload-wrapper.o 0xe0307c90 0x100 0xe0300000

bash scripts/inspect-arm-window.sh \
  build/driver-analysis-decoded/arm-payload-wrapper.o 0xe03225a0 0x80 0xe0300000
```

These windows should help distinguish executable instructions from pointer-table contents. Do not copy candidate initialization values into the hardware driver until the command-write functions and configuration flow are understood.
