# Linux feasibility assessment

**Current status: undecided. There is not yet enough evidence to claim that the target can boot Linux.**

The original firmware includes proprietary-looking `.drv`, `.mod`, and `.plg` artifacts. Prior local analysis reported at least one ARM ELF, but public reverse-engineering notes for related ATJ227x devices and the Actions ActSDK identify a MIPS 4KEc / µC/OS-II environment. That conflict is unresolved for this exact X7 MP5; see [ISA/runtime discrepancy](ISA_RUNTIME_DISCREPANCY.md). Neither Linux feasibility nor impossibility should be asserted until the SoC marking and original ELF headers are verified. The core, memory map, MMU support, boot protocol and available kernel/BSP must be established.

## Evidence needed for a Linux go/no-go decision

### Boot and CPU
- Verified SoC and core revision.
- Boot ROM behavior, accepted image format, load addresses, signature requirements, and recovery method.
- Core/ISA details, MMU/exception model, interrupt controller, timers, cache configuration and interrupt routing.
- Evidence of an existing Linux kernel or a feasible open/available BSP for the exact SoC.

### Memory and storage
- Physical RAM size, reserved regions and usable memory map.
- A working storage controller and boot path.
- Filesystem and partition layout; safe access to removable media.
- A way to load, log, and recover an experimental kernel without overwriting the original firmware.

### Minimum peripherals
- LCD initialization, framebuffer/display output and backlight.
- Button input mechanism and stable input events.
- Audio output path and clocking.
- Power, reset, battery monitoring and clean shutdown.
- USB/serial diagnostics where hardware exposes them.

## Minimum prototype gate

Do not integrate a frontend until all are true:
1. An experimental image can be loaded using a documented, recoverable path.
2. It reaches a diagnostic shell or minimal userspace.
3. Logs and a reliable reset/recovery procedure are available.
4. RAM and storage operate without corruption.
5. LCD, input and audio can be tested independently.

## Practical fallback

If full Linux bring-up proves infeasible, preserve the goal of improving the device without mislabeling the result: investigate changes to the existing launcher/configuration, reusable emulator cores that fit the original runtime, and UI/theme work compatible with the stock firmware. Keep that path distinct from a Linux/MiyooCFW port.
