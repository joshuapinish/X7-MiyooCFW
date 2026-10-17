# X7-MiyooCFW — Development Roadmap

**Status:** Experimental research and hardware bring-up  
**Target:** X7 / MP5 handheld revisions; Actions Semiconductor ATJ2273B or ATJ2273S are candidates to verify, not a universal specification for every device branded X7.  
**Goal:** Develop the most capable alternative firmware that the verified target hardware can support.

## Objectives

- Identify hardware revisions and establish a compatibility matrix.
- Preserve and analyze original firmware and removable media.
- Document boot flow, memory layout, display, audio, controls, and storage.
- Investigate alternative firmware architectures rather than assume Linux compatibility.
- Improve the interface and game-library management if the platform permits it.
- Evaluate emulator compatibility and performance against real benchmarks.
- Establish and test a safe recovery procedure before any firmware-writing experiment.

## Repository structure

```text
X7-MiyooCFW/
├── README.md
├── ROADMAP.md
├── docs/
│   ├── HARDWARE.md
│   ├── COMPATIBILITY.md
│   ├── BOOT_PROCESS.md
│   ├── FIRMWARE_ANALYSIS.md
│   └── LINUX_FEASIBILITY.md
├── research/
│   └── REFERENCES.md
├── tools/
│   └── README.md
├── firmware/
│   └── README.md
├── ui/
│   └── README.md
└── tests/
    └── README.md
```

## Milestones

### M0 — Preserve the baseline and inventory evidence
- [x] Extract original firmware for analysis.
- [x] Record a full-card image path and observed image size.
- [x] Collect an initial listing from a PC-accessible FAT volume.
- [ ] Record SHA-256 for the image and verify the backup against its source or a second independent read.
- [ ] Record which physical medium is boot media, removable game storage, or USB-exposed storage.

### M1 — Identify the exact hardware revision
- [ ] Read the SoC marking from the board or obtain an unambiguous silicon/firmware identifier.
- [ ] Record board revision, RAM package/size, flash/SD topology, LCD marking, and connector/pin details.
- [ ] Build a compatibility matrix instead of treating all X7 devices as identical.

### M2 — Complete original-firmware analysis
- [ ] Inventory image partitions, headers, boot-related blobs, and all executable formats.
- [ ] Determine executable ABI, CPU instruction set, memory assumptions, and runtime environment.
- [ ] Trace how the menu starts each emulator and how display, audio, input, and storage are accessed.
- [ ] Document findings with exact file paths, offsets, hashes, and reproducible commands.

### M3 — Document boot and peripheral behavior
- [ ] Identify Boot ROM / first-stage loader / second-stage loader / kernel or proprietary runtime, if present.
- [ ] Capture boot logs through a confirmed interface if available.
- [ ] Establish LCD initialization, input scanning, audio output, power, and storage behavior.
- [ ] Do not write to flash or boot media during reconnaissance.

### M4 — Feasibility decision
- [ ] Decide whether the hardware can support Linux and what public or reconstructable boot chain exists.
- [ ] Assess kernel/BSP, RAM, MMU, storage, LCD, audio, GPIO/input, and power support.
- [ ] Choose between a full Linux port, portable userspace/application reuse, or modifications to the existing firmware.
- [ ] Document evidence for a go/no-go decision.

### M5 — Minimal prototype
- [ ] Build a reproducible host toolchain.
- [ ] Produce a testable artifact without overwriting original media.
- [ ] Define a recovery plan before first boot attempt.
- [ ] Test the earliest stage that can be validated independently.

### M6 — Peripheral validation
- [ ] Display init and stable frame output.
- [ ] Button/input mapping and repeat behavior.
- [ ] Audio output, sample rate, latency, and stability.
- [ ] SD/filesystem reads, writes, shutdown, and save integrity.

### M7 — UI and emulator integration
- [ ] Evaluate lightweight frontends and emulator cores against available RAM/CPU performance.
- [ ] Implement library scanning and metadata without bundling commercial ROMs.
- [ ] Measure frame pacing, audio quality, and power/thermal behavior on the target.

### M8 — Recovery and release
- [ ] Validate recovery independently of the test image.
- [ ] Publish reproducible build steps, hardware matrix, known issues, checksums, and tested revision identifiers.
- [ ] Release only redistributable project artifacts and original/modified material whose license permits distribution.

## Safety requirements

- Never assume all X7 devices share the same motherboard or SoC.
- Never flash an image solely because its filename mentions X7.
- Keep an untouched original backup and record its SHA-256, size, origin, and verification method.
- Do not begin firmware flashing before a practical recovery path has been demonstrated.
- Keep facts, hypotheses, and unknowns visibly separate in documentation.
