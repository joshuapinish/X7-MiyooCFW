# Boot-process investigation

**Status: unknown. No bootloader replacement or firmware flashing is authorized by the current evidence.**

## Questions to answer

1. What medium contains the boot chain: soldered flash, SD card, or a combination?
2. What does the SoC Boot ROM load, and through which interface?
3. Are images signed, checksummed, compressed, encrypted, or wrapped in a vendor container?
4. Is the runtime a Linux kernel, an RTOS, or a proprietary environment?
5. Is there a serial console, USB recovery mode, key-combination recovery path, or vendor flashing protocol?
6. Can code be booted from removable media without modifying persistent storage?

## Read-only evidence collection order

1. Preserve and hash the existing card image; verify size and the backup method.
2. Inventory all physical devices with `lsblk -o NAME,PATH,SIZE,FSTYPE,LABEL,UUID,RO,RM,TRAN,MODEL,MOUNTPOINTS`.
3. Identify the observed FAT volume and the separate SD/MMC device from USB descriptors and device unplug/replug behavior. Never infer identity from `/dev/sdX` names alone.
4. Parse firmware/container headers and partition tables on copies or read-only mounts.
5. Search original configuration and binaries for boot arguments, loader names, load addresses, recovery strings, update commands, USB IDs, and image signatures.
6. Inspect any physically exposed UART only after identifying safe voltage levels and pinout. Never connect a 3.3 V USB-UART adapter to an unknown-voltage pin.
7. Record all observations with file offsets, tool versions, hashes, and exact hardware revision.

## Minimum recovery gate

Before any write or boot experiment, record:
- a verified original image and its SHA-256;
- a second copy on a separate physical disk;
- the exact target device identity and write-protection state;
- the restore command prepared but not executed against an ambiguous device;
- evidence that the recovery procedure can restore the original state.

A successful file listing over USB does not establish where the system boots from.
