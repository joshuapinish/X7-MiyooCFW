# First fire-test campaign

This campaign is read-only. It inventories the already-extracted firmware, inspects executable metadata and high-signal strings, extracts relevant configuration sections, compares a local MiyooCFW checkout, and samples headers from the PC-visible game volume without copying ROM data.

## Run on Void Linux

    cd ~/X7-FirmwareLab
    python3 tools/x7_firetest.py \
      --project "$HOME/X7-FirmwareLab" \
      --miyoo "$HOME/X7-FirmwareLab/MiyooCFW" \
      --volume "/run/media/joshua/3EDF-BD13" \
      --image "$HOME/sd-backup-completo.img"

Adjust arguments to match actual paths. Do not infer device identity from /dev/sdX names.

To hash the entire multi-gigabyte image, add --hash-image. The default does not read the entire image.

## Reports

- SUMMARY.md: run summary and reading order.
- 00-environment.txt: host and utility availability.
- 01-host-and-usb.txt: block-device table, mount information, USB devices and host kernel log. It is not the console boot log.
- 02-miyoo-checkout.txt: local upstream source checkout, revision and submodule state.
- 03-firmware-inventory.tsv: extracted files, sizes and extensions.
- 04-binary-signatures.txt: first 64 bytes for candidate executable artifacts.
- 05-executable-analysis.txt: file/readelf output, ELF headers, ARM attributes and SHA-256.
- 06-interesting-strings.txt: launch, runtime, LCD, audio, input and platform clues.
- 07-config-and-launch-paths.txt: relevant app_config.fex sections and launcher descriptors.
- 08-volume-and-kg.txt: top-level storage, GAME_MEMORY bytes, sample .KG headers only.
- 09-image-check.txt: image metadata and first sector; full hash only when requested.

## Questions this should answer

1. Are application files actual ELF files, and what do their headers say about ELF class, endian, machine, ABI and load segments?
2. Do strings point to Linux, libc, SDL, framebuffer/ioctl or a proprietary runtime?
3. Which launch conventions connect the home/explorer menu with game_*.axf?
4. Where are LCD initialization tables and panel settings referenced?
5. Does the extracted image contain a recognizable kernel or bootloader?
6. Are .KG files ROMs, wrapped containers, or not yet identified?
7. Which MiyooCFW components are Linux-specific and therefore cannot simply be copied into the existing runtime?

## Safety

The script does not write, partition, format or flash the handheld volume. Do not commit full firmware images, commercial ROMs, proprietary blobs or secrets. Inspect reports for private paths and device identifiers before sharing them.
