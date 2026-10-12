#!/usr/bin/env bash
set -Eeuo pipefail

usage() {
    printf 'Usage: bash %s <original-display.drv ELF> [output-directory]\n' "$0" >&2
    printf 'Example: bash %s ../extracted/original-fat16/drv/display.drv build/driver-analysis\n' "$0" >&2
}

if [[ $# -lt 1 || $# -gt 2 ]]; then
    usage
    exit 2
fi

input=$1
out=${2:-build/driver-analysis}

if [[ ! -f "$input" ]]; then
    printf 'ERROR: input file not found: %s\n' "$input" >&2
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

if [[ -z "$READELF" || -z "$OBJDUMP" || -z "$STRINGS" ]]; then
    printf 'ERROR: need readelf, objdump and strings (GNU binutils or LLVM tools).\n' >&2
    exit 2
fi

{
    printf 'Input: %s\n' "$input"
    printf 'SHA256: '
    sha256sum "$input" | awk '{print $1}'
    printf 'File type: '
    file "$input"
    printf 'readelf: %s\nobjdump: %s\nstrings: %s\n' "$READELF" "$OBJDUMP" "$STRINGS"
} > "$out/metadata.txt"

"$READELF" -hW "$input" > "$out/elf-header.txt" 2>&1 || true
"$READELF" -lW "$input" > "$out/program-headers.txt" 2>&1 || true
"$READELF" -SW "$input" > "$out/sections.txt" 2>&1 || true
"$READELF" -sW "$input" > "$out/symbols.txt" 2>&1 || true
"$STRINGS" -a -t x -n 4 "$input" > "$out/strings.txt"

grep -Ein 'LCD_HSD045F8W7|9806E|lcd0_para|lcd_bl_en_used|lcd_pwm_used|lcdclk|lcdde|lcdhsync|lcdvsync|SPIWRITE|SPI_WriteComm|fetch script data|display|backlight|pwm|reset' \
    "$out/strings.txt" > "$out/display-strings.txt" || true

if ! "$OBJDUMP" -drwC -M reg-names-std "$input" > "$out/disassembly.txt" 2> "$out/objdump-errors.txt"; then
    if ! "$OBJDUMP" -drwC "$input" > "$out/disassembly.txt" 2>> "$out/objdump-errors.txt"; then
        printf 'ERROR: objdump could not disassemble this file.\n' >&2
        printf 'Selected objdump: %s\n' "$OBJDUMP" >&2
        cat "$out/objdump-errors.txt" >&2
        printf 'Metadata and strings are still saved under %s\n' "$out" >&2
        exit 1
    fi
fi

printf '\nAnalysis written to: %s\n' "$out"
printf '\n=== ELF architecture ===\n'
grep -E 'Class:|Data:|Type:|Machine:|Entry point address:' "$out/elf-header.txt" || true
printf '\n=== Display-related strings ===\n'
cat "$out/display-strings.txt"
printf '\nNext: inspect elf-header.txt, sections.txt and disassembly.txt around the string references.\n'
