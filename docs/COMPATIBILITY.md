# Compatibility assessment

## Current conclusion

**A stock MiyooCFW image is not established as compatible with this X7 MP5 and must not be flashed to it.**

The upstream MiyooCFW wiki states that supported devices use Allwinner F1C100S or F1C500S SoCs and lists the Powkiddy X7 as *not confirmed*. The X7 MP5 in this project is being investigated as an Actions Semiconductor ATJ227x device. The shared “X7” name does not establish that these products use the same motherboard or processor. See [upstream compatibility notes](https://github.com/TriForceX/MiyooCFW/wiki/).

## Compatibility matrix

| Component | Current status | Evidence needed |
|---|---|---|
| Exact X7 MP5 SoC | Candidate: Actions ATJ2273B / ATJ2273S | Physical marking or reliable silicon identifier. |
| MiyooCFW boot image | Not compatible by assumption; untested | A supported boot chain and board-specific image format must be established. |
| CPU/ISA and runtime | Prior local analysis reported an ARM ELF, but related ATJ227x reverse-engineering references identify MIPS 4KEc and µC/OS-II | Re-run readelf on the original app/driver ELFs and verify the physical SoC marking; resolve this contradiction before choosing a toolchain. |
| Linux kernel support | Unknown | Find a usable kernel/BSP or prove a feasible board port with required drivers. |
| Bootloader / boot process | Unknown | Recover image layout and boot logs; identify signature, packaging, and load-address requirements. |
| LCD | Partially identified by driver strings | Reconstruct initialization, timings, pixel format, framebuffer path, and backlight control. |
| Audio | Original driver artifacts exist | Determine hardware interface and whether any usable Linux or userland API exists. |
| Controls | Original input driver artifacts exist | Decode key mapping and identify GPIO/ADC/input mechanism. |
| Storage | FAT32 game volume observed | Establish actual storage device topology and boot/update mechanism. |
| Portable applications/frontends | Potential reuse only | Check libc, kernel interfaces, architecture, dependencies, and memory/CPU budget. |

## ISA/runtime blocker

See [ISA/runtime discrepancy](ISA_RUNTIME_DISCREPANCY.md). A public reverse-engineering account for related ATJ227x hardware describes µC/OS-II, MIPS-targeted ELF applications and an Actions-specific runtime. The user's exact SoC and the previously reported ARM ELF driver have not yet been reconciled. This is a high-priority evidence gap, not a proven impossibility result.

## Strategy branches

1. **If a supported Linux boot chain/kernel can be established:** build a board-specific image and port missing drivers, keeping MiyooCFW frontend/emulator components only where ABI and resource limits permit.
2. **If Linux is technically possible but no usable BSP exists:** first prove boot and memory support, then implement minimum storage, LCD, input, audio, and power drivers before integrating a frontend.
3. **If Linux is not feasible with available evidence/resources:** prioritize safe modifications to the original firmware, a replacement UI within its runtime, or portable emulator/application components. Do not call this a full MiyooCFW port.

No branch is selected yet; the feasibility decision depends on verified hardware and boot evidence.
