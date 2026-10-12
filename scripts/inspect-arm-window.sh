#!/usr/bin/env bash
set -Eeuo pipefail

usage() {
    printf 'Usage: %s <analysis-wrapper.o> <start-address-hex> [byte-count-hex] [load-address-hex]\n' "$0" >&2
    printf 'Example: %s build/driver-analysis-decoded/arm-payload-wrapper.o 0xe0307c90 0x100 0xe0300000\n' "$0" >&2
    exit 2
}

[[ $# -ge 2 && $# -le 4 ]] || usage
object=$1
start=$2
count=${3:-0x100}
base=${4:-${X7_DRIVER_BASE:-0xe0300000}}
objdump=${OBJDUMP:-$(command -v arm-none-eabi-objdump || command -v llvm-objdump || command -v objdump || true)}

[[ -f "$object" ]] || { echo "ERROR: object not found: $object" >&2; exit 2; }
[[ -n "$objdump" ]] || { echo "ERROR: no objdump found" >&2; exit 2; }
[[ "$start" =~ ^0[xX][0-9a-fA-F]+$ ]] || { echo "ERROR: start must be hex, e.g. 0xe0307c90" >&2; exit 2; }
[[ "$count" =~ ^0[xX][0-9a-fA-F]+$ ]] || { echo "ERROR: length must be hex, e.g. 0x100" >&2; exit 2; }
[[ "$base" =~ ^0[xX][0-9a-fA-F]+$ ]] || { echo "ERROR: load address must be hex" >&2; exit 2; }

start_num=$((start))
count_num=$((count))
base_num=$((base))

if (( start_num < base_num )); then
    printf 'ERROR: start address 0x%x is below assumed load base 0x%x\n' "$start_num" "$base_num" >&2
    exit 2
fi

# The synthetic ELF is ET_REL with .text at VMA 0. Ask objdump for a section-
# relative window first; add the assumed runtime base to printed address labels
# afterwards. This avoids tool-specific ambiguity about when --adjust-vma is
# applied relative to --start-address/--stop-address.
section_start=$((start_num - base_num))
section_stop=$((section_start + count_num))
absolute_stop=$((start_num + count_num))

printf 'Tool: %s\n' "$objdump"
printf 'Requested VA range: 0x%x .. 0x%x\n' "$start_num" "$absolute_stop"
printf 'Section-relative range: 0x%x .. 0x%x\n' "$section_start" "$section_stop"
printf 'Assumed load base: 0x%x\n' "$base_num"
printf 'NOTE: blind disassembly window; literal pools/data may be decoded as instructions.\n\n'

"$objdump" -D -j .text -M reg-names-std \
    --start-address="$section_start" --stop-address="$section_stop" "$object" |
python3 -c '
import re, sys
base = int(sys.argv[1])
for line in sys.stdin:
    match = re.match(r"^(\s*)([0-9a-fA-F]+):(.*)$", line.rstrip("\\n"))
    if match:
        address = int(match.group(2), 16) + base
        print(f"{match.group(1)}{address:08x}:{match.group(3)}")
    else:
        print(line, end="")
' "$base_num"
