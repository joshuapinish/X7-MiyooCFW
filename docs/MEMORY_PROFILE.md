# RAM profile
Configure expected target RAM through `X7_RAM_MIB`. Supported integer values are 32 through 256 MiB inclusive.

```sh
cmake -S . -B build-32  -DX7_RAM_MIB=32
cmake -S . -B build-64  -DX7_RAM_MIB=64
cmake -S . -B build-128 -DX7_RAM_MIB=128
cmake -S . -B build-256 -DX7_RAM_MIB=256
```

This is a build-time profile only. It does not detect installed RAM, establish the physical memory map, reserve framebuffer memory, or modify a kernel. Do not commit a hardware memory map until board revision and RAM layout are confirmed.

For a 480x854 framebuffer, estimated raw storage is:
- RGB565: 821,760 bytes (about 0.78 MiB).
- 32-bit pixels: 1,643,520 bytes (about 1.57 MiB).

Double buffering doubles these values before alignment and other graphics allocations.
