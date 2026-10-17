# User interface

UI and library-management work depends on the feasibility result.

Before implementing a full frontend, establish:
- the runtime or operating system that will host it;
- available RAM, CPU performance, display mode and input API;
- how games are launched and how emulator processes return to the menu;
- safe save/configuration paths and clean-shutdown behavior.

Prefer a lightweight, modular interface that can be reused if the platform supports Linux. Keep UI experiments separate from any bootloader, kernel, or persistent firmware changes. Do not bundle commercial ROMs or copyrighted vendor artwork without permission.
