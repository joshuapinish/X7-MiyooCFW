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
stop_num=$((start_num + count_num))

printf 'Tool: %s\nRange: %s .. 0x%x\nLoad-address adjustment: %s\n' \
    "$objdump" "$start" "$stop_num" "$base"
printf 'NOTE: blind disassembly window; literal pools/data may be decoded as instructions.\n\n'

"$objdump" -D -M reg-names-std --adjust-vma="$base" \
    --start-address="$start" --stop-address="0x$(printf '%x' "$stop_num")" "$object"
