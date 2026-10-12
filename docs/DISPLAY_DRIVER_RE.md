# Recovering the original X7 display driver

The source of truth for the board's panel initialization is the original driver and its configuration, not a generic ILI9806E example.

## Run the local analysis

From the X7 MiyooCFW checkout, assuming the extraction directory is a sibling under `~/X7-FirmwareLab`:

```sh
bash scripts/analyze-arm-driver.sh \
  ../extracted/original-fat16/drv/display.drv \
  build/driver-analysis
```

The script does not modify the original binary. It records the input SHA-256, ELF header, program headers, sections, symbols, printable strings and available disassembly under `build/driver-analysis/`.

For a raw decoded payload, use the original `drv/display.drv` ELF first. The payload may no longer carry ELF section/virtual-address information, so its offsets cannot safely be treated as link-time addresses.

## Required evidence before writing a physical init table

Extract and document:
- exact command/data transport and whether command/data are sent by SPI or a parallel LCD interface;
- GPIO/pin assignments and active polarity for reset, panel enable and backlight;
- panel reset timing and complete controller command/data sequence;
- pixel format, orientation, lane/bus mode, porches, sync polarities, pixel clock and refresh rate;
- the configuration object/file used by the driver's `lcd0_para`, `lcd_bl_en_used` and `lcd_pwm_used` lookups.

The known identifier is `LCD_HSD045F8W7_9806E__4_5`. Do not assume a string offset in the ELF equals its runtime address; use ELF section offsets and virtual addresses. Do not enable the backlight until panel power/reset sequencing is understood.

## MiyooCFW platform compatibility

The upstream MiyooCFW porting docs reference an Allwinner suniv/F1C500S kernel/device tree and a matching U-Boot configuration. This is not a drop-in kernel for an Actions ATJ227X board. Reusing MiyooCFW's userspace, Buildroot recipes or emulators may be possible after a compatible Linux boot chain, kernel port and board support exist. The original display driver being ARM ELF only confirms its instruction-set ABI, not Linux API compatibility.

References:
- MiyooCFW build guide: https://github.com/TriForceX/MiyooCFW/wiki/Build-Source-DEPRECATED
- MiyooCFW repository: https://github.com/TriForceX/MiyooCFW
- ATJ227X reverse-engineering notes: https://pulkomandy.tk/_/_Electronique/_Reverse%20Engineering%20notes%20for%20ATJ227x
