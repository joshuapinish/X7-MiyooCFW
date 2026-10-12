# Recovering the original X7 display driver

The source of truth for the board's panel setup is the original driver and its configuration, not a generic ILI9806E example.

## Important: original driver vs decoded payload

The original `extracted/original-fat16/drv/display.drv` is only 56,252 bytes. Its ELF section table describes an executable section of `0x344f4` bytes (214,260 bytes), larger than the file itself. The bulk-decoded payload has exactly 214,260 bytes and contains the display identifier and related configuration strings. Treat the original file as a custom ePOS module/container rather than passing it directly to a normal ELF disassembler.

## Run the local analysis on the decoded ARM payload

From `~/X7-FirmwareLab/X7-MiyooCFW-test`:

```sh
git pull --ff-only origin x7-port
bash scripts/analyze-arm-driver.sh \
  ../extracted/bulk-decoded/drv__display.drv.payload.bin \
  build/driver-analysis-decoded
```

The script records the input SHA-256, strings and ARM disassembly. For a raw payload, it creates a temporary ELF wrapper at `build/driver-analysis-decoded/arm-payload-wrapper.o` so GNU/LLVM objdump can decode ARM instructions. That wrapper exists **only for analysis** and is not a bootable binary. The default display-driver load address comes from the original ELF entry point, `0xe0300000`; override it using `X7_DRIVER_BASE=0x...` only if new evidence supports a different address.

Useful reports:
- `metadata.txt`: input identity, hash and analysis mode.
- `display-strings.txt`: relevant strings with offsets in the raw payload.
- `disassembly.txt`: ARM disassembly using the assumed load address.
- `elf-header.txt` and `sections.txt`: temporary ARM analysis-object metadata.

Next, scan for literal absolute pointers to the relevant strings:

```sh
python3 scripts/find-arm-string-xrefs.py \
  ../extracted/bulk-decoded/drv__display.drv.payload.bin
```

This is a heuristic scan: ARM code can also form addresses with PC-relative loads or split immediates, so a missing literal pointer does not prove a string is unused.

## What must be recovered before the panel driver is made hardware-active

- exact command/data transport and whether command/data are sent by SPI or a parallel LCD interface;
- GPIO/pin assignments and active polarity for reset, panel enable and backlight;
- panel reset timing and full controller command/data sequence;
- pixel format, orientation, bus mode, porches, sync polarities, pixel clock and refresh rate;
- the configuration object/file used by the driver's `lcd0_para`, `lcd_bl_en_used` and `lcd_pwm_used` lookups.

The firmware contains the identifier `LCD_HSD045F8W7_9806E__4_5`. Do not assume a string offset equals its runtime address unless the load address and mapping are verified. Keep physical reset/backlight operations disabled until power sequencing is understood.

## MiyooCFW platform compatibility

MiyooCFW's existing board support is not a drop-in kernel for an Actions ATJ227X board. Reusing userland/Buildroot recipes may be feasible after a compatible Linux boot chain, kernel port and board support exist. The original driver being ARM ELF family only confirms the instruction-set ABI, not Linux API compatibility.

References:
- MiyooCFW build guide: https://github.com/TriForceX/MiyooCFW/wiki/Build-Source-DEPRECATED
- MiyooCFW repository: https://github.com/TriForceX/MiyooCFW
- ATJ227X reverse-engineering notes: https://pulkomandy.tk/_/_Electronique/_Reverse%20Engineering%20notes%20for%20ATJ227x
