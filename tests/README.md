# Test plan

Track every result by exact device revision, source commit, configuration and test conditions. Mark each test as **not run**, **pass**, **fail**, or **blocked**.

## Host-side tests
- Build portable project code.
- Run unit tests and static analysis.
- Validate parsers against synthetic/corrupt inputs.
- Check report generation and artifact hash manifests.

## Hardware tests (only after safe instrumentation is established)
- [ ] SoC and board revision identified.
- [ ] Original image backup verified and recovery path recorded.
- [ ] LCD initialization and stable frame output.
- [ ] Button mapping, repeat, simultaneous inputs and debounce.
- [ ] Audio channels, supported rates, latency and sustained playback.
- [ ] Storage read/write integrity and save persistence.
- [ ] Power-off, reset, suspend/wake and battery behavior.
- [ ] Emulator frame pacing and audio/video synchronization.

No destructive test is considered acceptable until a recovery path has been demonstrated independently.
