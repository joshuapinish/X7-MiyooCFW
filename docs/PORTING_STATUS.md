# X7 porting status

## Phase 0: host-buildable scaffold
- [x] Initialize the remote port branch.
- [x] Add a platform-neutral C display-bus interface.
- [x] Add a bounded command-sequence executor with error propagation.
- [x] Add mock-bus unit tests.
- [x] Add a configurable 32–256 MiB build profile.
- [x] Add CI for compile/test checks.
- [ ] Verify results in GitHub Actions and on the local Void Linux toolchain.

## Phase 1: original-firmware extraction
- [ ] Confirm the exact ATJ227X part/revision and board RAM size.
- [ ] Disassemble the original `display.drv` around configuration lookup and panel setup.
- [ ] Recover bus type, pin assignments, reset polarity, pixel format, timings, and init commands.
- [ ] Trace `lcd0_para`, `lcd_bl_en_used`, and `lcd_pwm_used` reads to their actual config source.
- [ ] Verify that 480x854 is the active mode.
- [ ] Confirm backlight PWM and panel-enable polarity.

## Phase 2: firmware feasibility
- [ ] Identify boot ROM/bootloader and whether Linux can boot on this exact SoC.
- [ ] Confirm whether a usable Linux BSP/kernel exists; ARM alone does not prove this.
- [ ] Determine physical RAM map and reserved memory before setting boot arguments.
- [ ] Select a compatible MiyooCFW Buildroot/kernel base or document the blocker.

## Phase 3: hardware image
- [ ] Implement the panel-specific sequence only after recovering it.
- [ ] Add real board GPIO/bus operations.
- [ ] Build a reproducible, checksummed SD test image.
- [ ] Test from a recoverable copy/card, preserving the original full-card image.

The present tests use a mock bus. They do not access the physical LCD and do not produce a flashable firmware image.
Panel dimensions and controller family remain candidates pending verification against the exact panel and active mode.
