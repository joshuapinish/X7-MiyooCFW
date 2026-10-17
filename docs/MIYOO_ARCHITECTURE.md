# MiyooCFW architecture and port implications

This note separates upstream MiyooCFW architecture from what has actually been verified on the X7 MP5.

## What MiyooCFW contains

The upstream repository uses separate submodules for:

- U-Boot
- Linux kernel
- Buildroot userspace/root filesystem
- GMenu2X frontend and skins
- Daemon and control tools such as miyooctl
- Logo/assets

Source: [upstream .gitmodules](https://github.com/TriForceX/MiyooCFW/blob/master/.gitmodules), [upstream repository](https://github.com/TriForceX/MiyooCFW).

The legacy upstream build guide documents an Allwinner-specific boot path using a suniv U-Boot configuration, a Linux kernel device tree named `suniv-f1c500s-miyoo.dts`, zImage, DTB, boot.scr and a Buildroot root filesystem. Its example boot script loads the kernel and device tree at fixed addresses and passes Linux boot arguments. Those addresses, board config, DTB and boot script are examples for the supported Allwinner hardware, **not values to copy onto the Actions ATJ227x target**.

Reference: [MiyooCFW legacy build guide](https://github.com/TriForceX/MiyooCFW/wiki/Build-Source-DEPRECATED).

Upstream releases have used uClibc and musl rootfs builds. An executable compiled for one of these environments is not automatically compatible with the X7's original runtime, even if both CPUs execute ARM instructions.

## Critical X7 ISA/runtime uncertainty

Public reverse-engineering notes for related Actions ATJ227x hardware describe MIPS-targeted ELF applications running under µC/OS-II, and the public ActSDK identifies a MIPS 4KEc target. Prior local analysis of this project's original display driver reported ARM ELF/EABI4. Those results conflict and the exact X7 MP5 SoC/revision is not yet verified. Consult [ISA/runtime discrepancy](ISA_RUNTIME_DISCREPANCY.md) and obtain the original files' readelf headers before selecting any cross-compiler or judging which binaries can be reused.

## What this means for our port

A full MiyooCFW port is not simply copying the menu or SD image to the X7. We must establish a compatible boot flow and kernel/platform layer first. The following are separate workstreams:

1. **Boot path:** determine whether the ATJ227x boot ROM and existing loaders can load a Linux kernel, and learn any required image/signature/container format.
2. **Kernel/BSP:** identify usable kernel support or determine the effort required for CPU, interrupts, timers, RAM map, storage and board support.
3. **Peripheral support:** bring up LCD, backlight, input, audio and power management.
4. **Userspace:** build a root filesystem for the actual CPU ABI, libc, storage layout and available RAM.
5. **Frontend/emulators:** port/rebuild GMenu2X-like UI and emulator cores only after the runtime and graphics/audio/input APIs exist.

Some application logic, UI resources, game metadata parsers and portable emulator code may be reusable. Existing X7 .axf programs may instead target the vendor's proprietary runtime and its driver APIs. ELF/ARM headers alone cannot distinguish these cases; imports, strings, launch protocol and runtime dependencies must be analyzed.

## High-value comparison tests

- Use readelf/file to identify ELF class, endianness, machine, EABI, entry point, program segments and ARM attributes for original apps and drivers.
- Look for evidence of Linux interfaces such as /proc, /sys, framebuffer ioctls, SDL and libc; absence of strings is not proof of absence.
- Trace the original launcher-to-emulator handoff and required command line, working directory, file extensions and save path.
- Identify and inspect epos.img as data, without assuming the extension means a kernel or a complete firmware image.
- Compare the X7 board's verified SoC/revision against the Allwinner-only assumptions in the MiyooCFW boot scripts, DTBs and kernel configuration.
- Do not reuse Miyoo boot addresses, device trees, root partition numbering or U-Boot configuration unless hardware evidence independently supports them.

## Decision outcomes

- **Linux boot path and usable platform support found:** build a board-specific image and replace/port the drivers that differ.
- **Linux possible but no usable board support:** create a minimum kernel bring-up plan; do not integrate a frontend yet.
- **No practical Linux path:** investigate safe changes to the vendor environment, including launcher/configuration changes and separately rebuilt applications where ABI and driver access permit.
