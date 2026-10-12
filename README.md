# X7 MiyooCFW port

Experimental porting workspace for the X7 MP5 handheld.

**Status: bring-up scaffold, not a flashable firmware image.** This project currently establishes a host-buildable display-driver interface and automated tests before hardware-specific register sequences or a boot image are attempted.

## Hardware findings

- Original firmware contains the panel driver identifier `LCD_HSD045F8W7_9806E__4_5`.
- The controller is being investigated as an ILI9806E-family device. Panel timing, bus wiring, reset polarity, command table, and pixel format still need confirmation against the original driver and the physical board.
- The original display driver is a 32-bit little-endian ARM ELF (EABI4).
- ARM instruction compatibility does **not** establish Linux kernel, bootloader, or MiyooCFW compatibility.

## RAM target

Support a configurable range from 32 MiB to 256 MiB. Do not assume every X7 unit has 256 MiB. Runtime reservations and kernel/userspace limits depend on a confirmed memory map.

## Host build

```sh
cmake -S . -B build -DX7_BUILD_TESTS=ON
cmake --build build
ctest --test-dir build --output-on-failure
```

This validates the portable display core only. It does not initialize the physical LCD or produce bootable firmware.

## Bring-up plan

1. Compile and test the portable display core.
2. Recover the real init table and bus configuration from the original ARM driver.
3. Confirm exact SoC revision, boot chain, RAM map, and peripherals.
4. Select/port a matching Linux kernel and Buildroot configuration.
5. Integrate the verified panel driver and create a recoverable SD test image.
6. Test from removable media while preserving the original full-card image.

Never flash a generated image to the original card until the boot chain and recovery procedure are understood.
