# Firmware artifacts

This directory is reserved for project-generated, redistributable firmware components and documented patches.

Do not commit:
- the complete original SD/firmware image;
- vendor executables or proprietary driver blobs unless redistribution is explicitly permitted;
- encryption keys, secrets, device-specific credentials or private dumps;
- commercial game ROMs or packaged game libraries.

Prefer source patches, configuration diffs, build scripts, small independently redistributable test assets and instructions that allow users to provide their own original files. Every binary release must identify its target board revision, source commit, build method and SHA-256 checksum.
