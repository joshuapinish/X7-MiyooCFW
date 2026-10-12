#!/usr/bin/env bash
set -Eeuo pipefail

usage() {
    printf 'Usage: bash %s <original-ELF-or-decoded-ARM-payload> [output-directory]\n' "$0" >&2
    printf 'Default raw-payload load address: 0xe0300000 (override with X7_DRIVER_BASE)\n' >&2
    printf 'Example: bash %s ../extracted/bulk-decoded/drv__display.drv.payload.bin build/driver-analysis\n' "$0" >&2
}

if [[ $# -lt 1 || $# -gt 2 ]]; then
    usage
    exit 2
fi

input=$1
out=${2:-build/driver-analysis}
base=${X7_DRIVER_BASE:-0xe0300000}

if [[ ! -f "$input" ]]; then
    printf 'ERROR: input file not found: %s\n' "$input" >&2
    exit 2
fi

if ! [[ "$base" =~ ^(0x)?[0-9a-fA-F]+$ ]]; then
    printf 'ERROR: X7_DRIVER_BASE must be a hexadecimal address (example: 0xe0300000).\n' >&2
    exit 2
fi

mkdir -p "$out"
input=$(realpath "$input")
out=$(realpath "$out")

pick_tool() {
    local candidate
    for candidate in "$@"; do
        if command -v "$candidate" >/dev/null 2>&1; then
            command -v "$candidate"
            return 0
        fi
    done
    return 1
}

READELF=$(pick_tool arm-none-eabi-readelf arm-linux-gnueabi-readelf arm-linux-gnueabihf-readelf llvm-readelf readelf || true)
OBJDUMP=$(pick_tool arm-none-eabi-objdump arm-linux-gnueabi-objdump arm-linux-gnueabihf-objdump llvm-objdump objdump || true)
STRINGS=$(pick_tool strings llvm-strings || true)

if [[ -z "$OBJDUMP" || -z "$STRINGS" ]]; then
    printf 'ERROR: need an ARM-capable objdump and strings (GNU binutils or LLVM tools).\n' >&2
    exit 2
fi

magic=$(od -An -tx1 -N4 "$input" | tr -d '[:space:]')
is_elf=0
[[ "$magic" == "7f454c46" ]] && is_elf=1

{
    printf 'Input: %s\n' "$input"
    printf 'SHA256: '
    sha256sum "$input" | awk '{print $1}'
    printf 'File type: '
    file "$input"
    printf 'objdump: %s\nstrings: %s\n' "$OBJDUMP" "$STRINGS"
    if (( is_elf )); then
        printf 'Mode: ELF input\n'
    else
        printf 'Mode: decoded raw ARM payload\n'
        printf 'Assumed load address: %s\n' "$base"
    fi
} > "$out/metadata.txt"

"$STRINGS" -a -t x -n 4 "$input" > "$out/strings.txt"
grep -Ein 'LCD_HSD045F8W7|9806E|lcd0_para|lcd_bl_en_used|lcd_pwm_used|lcdclk|lcdde|lcdhsync|lcdvsync|SPIWRITE|SPI_WriteComm|fetch script data|display|backlight|pwm|reset' \
    "$out/strings.txt" > "$out/display-strings.txt" || true

if (( is_elf )); then
    if [[ -n "$READELF" ]]; then
        "$READELF" -hW "$input" > "$out/elf-header.txt" 2>&1 || true
        "$READELF" -lW "$input" > "$out/program-headers.txt" 2>&1 || true
        "$READELF" -SW "$input" > "$out/sections.txt" 2>&1 || true
        "$READELF" -sW "$input" > "$out/symbols.txt" 2>&1 || true
    fi

    if "$OBJDUMP" -drwC -M reg-names-std "$input" > "$out/disassembly.txt" 2> "$out/objdump-errors.txt"; then
        printf 'ELF disassembly written to %s/disassembly.txt\n' "$out"
    else
        cat "$out/objdump-errors.txt" >&2
        printf '\nThis ELF may be an ePOS module/container whose section sizes describe the decoded image, not its on-disk bytes.\n' >&2
        printf 'For this X7 display driver, rerun with the decoded payload file: drv__display.drv.payload.bin\n' >&2
        printf 'The original ELF was not changed. Strings and header reports remain in: %s\n' "$out" >&2
        exit 1
    fi
else
    if [[ -z "$READELF" ]]; then
        printf 'ERROR: readelf is needed to verify the temporary ARM object.\n' >&2
        exit 2
    fi

    wrapper="$out/arm-payload-wrapper.o"
    python3 - "$input" "$wrapper" <<'PY'
import struct
import sys
from pathlib import Path

source = Path(sys.argv[1])
target = Path(sys.argv[2])
payload = source.read_bytes()
if not payload:
    raise SystemExit("ERROR: decoded payload is empty")
if len(payload) % 4:
    print("WARNING: payload length is not a multiple of four; trailing bytes may be data.", file=sys.stderr)

# Construct a temporary ELF32 little-endian ARM relocatable object so LLVM/GNU
# objdump can disassemble a raw decoder output. This wrapper is analysis-only.
ident = b"\x7fELF" + bytes([1, 1, 1, 0, 0]) + bytes(7)
shstr = b"\x00.text\x00.shstrtab\x00"
ehdr_size = 52
text_offset = ehdr_size
strtab_offset = text_offset + len(payload)
shoff = (strtab_offset + len(shstr) + 3) & ~3
e_flags = 0x04000000  # ELF ARM EABI version 4, matching the source ELF family.
ehdr = struct.pack(
    "<16sHHIIIIIHHHHHH",
    ident, 1, 40, 1, 0, 0, shoff, e_flags,
    ehdr_size, 0, 0, 40, 3, 2
)
sh_null = bytes(40)
sh_text = struct.pack(
    "<IIIIIIIIII",
    1, 1, 0x6, 0, text_offset, len(payload), 0, 0, 4, 0
)
sh_strtab = struct.pack(
    "<IIIIIIIIII",
    7, 3, 0, 0, strtab_offset, len(shstr), 0, 0, 1, 0
)
result = bytearray(ehdr)
result.extend(payload)
result.extend(shstr)
result.extend(bytes(shoff - len(result)))
result.extend(sh_null)
result.extend(sh_text)
result.extend(sh_strtab)
target.write_bytes(result)
PY

    "$READELF" -hW "$wrapper" > "$out/elf-header.txt"
    "$READELF" -SW "$wrapper" > "$out/sections.txt"
    if ! "$OBJDUMP" -D -M reg-names-std --adjust-vma="$base" "$wrapper" > "$out/disassembly.txt" 2> "$out/objdump-errors.txt"; then
        cat "$out/objdump-errors.txt" >&2
        printf 'ERROR: the selected objdump could not disassemble the synthetic ARM wrapper.\n' >&2
        printf 'Try installing GNU ARM binutils or an LLVM build with the ARM target.\n' >&2
        exit 1
    fi
    printf 'Raw ARM payload was wrapped for analysis only; wrapper is NOT bootable firmware.\n' >> "$out/metadata.txt"
    printf 'ARM payload disassembly written to %s/disassembly.txt\n' "$out"
fi

printf '\nAnalysis written to: %s\n' "$out"
printf '\n=== Input summary ===\n'
cat "$out/metadata.txt"
printf '\n=== Display-related strings (file offsets) ===\n'
cat "$out/display-strings.txt"
printf '\n=== ELF architecture ===\n'
grep -E 'Class:|Data:|Type:|Machine:|Entry point address:' "$out/elf-header.txt" || true
printf '\nNOTE: for decoded raw input, the temporary ELF exists only to make disassemblers understand ARM code.\n'
