# X7 hardware bring-up and SD test policy

The target goal is a removable-SD hardware experiment, but there are two different software environments involved. Keep them separate until the exact SoC revision, instruction set and boot path are proven.

## What is established from the current evidence

- The original on-card `drv/display.drv` is a 56,252-byte custom ePOS module/container.
- Its ELF metadata describes an executable section of 214,260 bytes, matching the decoded payload size. Use `extracted/bulk-decoded/drv__display.drv.payload.bin` for reverse-engineering.
- The decoded payload contains `LCD_HSD045F8W7_9806E__4_5`, `lcd0_para`, `lcd_bl_en_used`, `lcd_pwm_used`, and strings related to SPI display writes.
- The decoded payload and MiyooCFW's kernel are not interchangeable artifacts. The MiyooCFW kernel/device-tree tree is for Allwinner suniv/F1C100S. This target board needs its own boot/kernel support before a MiyooCFW image could run.
- The decoded display payload is an ARM ELF32 little-endian/EABI4 code image. That is the strongest architecture evidence for this specific module.
- The public ActSDK LCD Makefile explicitly targets MIPS 4KEc with the SDE MIPS toolchain. Treat it as a reference for Actions' older LCD-driver design only, not as the compiler/build recipe for this ARM payload. A Linux kernel module also needs the exact target kernel ABI; an ARM ELF alone does not establish that ABI.

## The practical route to first hardware testing

### Track A: original-firmware/ePOS investigation

1. Recover the existing module's loader/packing path and ABI from the original firmware.
2. Trace the SPI write helper, panel-name lookup and `lcd0_para` table references in the decoded payload.
3. Establish the actual runtime CPU architecture and the matching compiler/SDK revision from the original firmware and SoC marking.
4. Recover the exact bus/pins and init sequence before altering the stock display module.
5. Build a separate test driver/module with a unique name, if the loader supports it. Do not replace the stock module on the first pass.
6. Stage it only on a separate test card/image and preserve the verified original image for recovery.

### Track B: MiyooCFW/Linux port

1. Confirm a viable Linux boot ROM/loader path for the exact X7 SoC.
2. Port or identify the required CPU, interrupt, timer, clock, pinctrl, RAM, SD/MMC, display engine, audio and input support.
3. Integrate an LCD driver against the selected kernel API only after those dependencies work.
4. Build a complete image and test it on a recoverable spare card.

Track B is not achieved by copying a Linux panel driver into MiyooCFW's source tree. Without a compatible kernel and boot chain, the SD image will not reach the point at which that driver can run.

## Safety rules for SD experiments

- Keep `/home/joshua/sd-backup-completo.img` unchanged and verify its SHA-256 against the recorded backup notes.
- Never target a block device (for example `/dev/sdX`) from an automated script in this repository.
- Generate artifacts into a staging directory first and review the manifest/hashes before manually copying to a spare card.
- The current portable `x7display` library and mock tests are not firmware, do not touch hardware, and are not an SD boot image.

## Relevant code and references

- Driver analysis: `scripts/analyze-arm-driver.sh`
- String pointer candidates: `scripts/find-arm-string-xrefs.py`
- Targeted disassembly windows: `scripts/inspect-arm-window.sh`
- Latest payload offsets: `docs/DISPLAY_ANALYSIS_NOTES_2026-10-12.md`
- Original driver report: `docs/DISPLAY_DRIVER_RE.md`
- MiyooCFW kernel: https://github.com/MiyooCFW/kernel/tree/add4deb177dfd8d2324650703f0014e9c862baa8
- MiyooCFW suniv board DTS: https://github.com/MiyooCFW/kernel/blob/add4deb177dfd8d2324650703f0014e9c862baa8/arch/arm/boot/dts/suniv-f1c100s-miyoo.dts
- Actions ActSDK LCD build recipe: https://github.com/mcirsta/ActSDK/blob/master/psp_rel/drivers/lcd/Makefile
- ATJ227x reverse-engineering notes: https://pulkomandy.tk/_/_Electronique/_Reverse%20Engineering%20notes%20for%20ATJ227x
