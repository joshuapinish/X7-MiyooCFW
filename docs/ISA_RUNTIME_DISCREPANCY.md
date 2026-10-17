# ISA and runtime discrepancy: mandatory verification

**Status: blocker for any serious port decision.** Do not choose an instruction set based on the product name or a secondary website.

## Evidence that conflicts

1. Prior local analysis recorded `drv/display.drv` as a 32-bit little-endian ARM ELF, EABI4, statically linked and stripped. This must be rechecked against the original file with `readelf -h -A`, not just inferred from its filename or a decoded payload's name.
2. Public reverse-engineering notes for related Actions ATJ227x devices identify an ATJ2279B platform, µC/OS-II, application ELF files and a MIPS toolchain: [ATJ227x reverse-engineering notes](https://pulkomandy.tk/_/_Electronique/_Reverse%20Engineering%20notes%20for%20ATJ227x).
3. The public [ActSDK](https://github.com/mcirsta/ActSDK) is described as an SDK for Actions SoCs running µC/OS; its application Makefile explicitly labels the processor as a MIPS 4KEc, 32-bit RISC, Actions board.
4. A third-party [ATJ2273B datasheet summary](https://www.datasheetcafe.com/atj2273b-pdf-datasheet-24428/) itself contains conflicting CPU descriptions, so that page alone cannot settle the exact ISA. The available ATJ227X datasheet is a family-level reference and its silicon revision/model applicability must be confirmed.

These sources are not proof that the user's exact X7 MP5 contains ATJ2279B or ATJ2273B/S. They do establish that an MIPS/µC/OS-II path is credible enough that the earlier ARM assumption must be checked before proceeding.

## Immediate test

Run this against the original extracted driver and the original applications, not only the files named `*.payload.bin`:

    cd ~/X7-FirmwareLab
    file extracted/original-fat16/drv/display.drv
    readelf -h -A extracted/original-fat16/drv/display.drv
    file extracted/original-fat16/apps/home.axf
    readelf -h -A extracted/original-fat16/apps/home.axf
    file extracted/original-fat16/apps/init.axf
    readelf -h -A extracted/original-fat16/apps/init.axf

Adjust paths if the files are stored elsewhere. For each valid ELF, record:
- ELF Class and Data (32/64-bit, little/big-endian);
- Machine field and ELF flags;
- ARM EABI attributes if it is ARM, or MIPS ABI/flags if it is MIPS;
- file path, SHA-256, and whether it is the original file or extracted payload.

If the direct original app/driver ELF files disagree about ISA, investigate whether they target different processors or execution environments. Do not combine their findings into one presumed runtime.

## Decision implications

- If the original application set is MIPS and tied to the Actions µC/OS runtime, MiyooCFW ARM/Linux binaries cannot run directly. The project would need a Linux port/BSP for the actual SoC or a stock-runtime modification route.
- If the original files are genuinely ARM and the exact chip is a different ISA variant, update the hardware identity and choose the corresponding toolchain only after the chip marking is confirmed.
- Linux feasibility remains open. A legacy µC/OS-II implementation does not by itself prove that Linux is architecturally impossible, but the boot chain, MMU, interrupt/timer support, memory map, and peripheral drivers would all need evidence.

Do not flash an image until this discrepancy and the target SoC identity are resolved.
