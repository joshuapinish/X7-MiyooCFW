#!/usr/bin/env bash
set -Eeuo pipefail

usage() {
    printf 'Usage: %s <analysis-wrapper.o> <start-address> [byte-count]\n' "$0" >&2
    printf 'Example: %s build/driver-analysis-decoded/arm-payload-wrapper.o 0xe0307c90 0x100\n' "$0" >&2
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
[[ "$start" =~ ^(0x)?[0-9a-fA-F]+$ ]] || { echo "ERROR: start must be hexadecimal" >&2; exit 2; }
[[ "$count" =~ ^(0x)?[0-9a-fA-F]+$ ]]
[[ "$base" =~ ^(0x)?[0-9a-fA-F]+$ ]] || { echo "ERROR: load address must be hexadecimal" >&2; exit 2; } || { echo "ERROR: length must be hexadecimal" >&2; exit 2; }

to_int() {
    local n=$1
    if [[ "$n" == 0x* || "$n" == 0X* ]]; then
        printf '%d' "$((n))"
    else
        printf '%d' "$((16#$n))"
    fi
}
start_num=$(to_int "$start")
count_num=$(to_int "$count")
base_num=$(to_int "$base")
stop_num=$((start_num + count_num))
printf 'Tool: %s\nRange: %s .. 0x%x\nNOTE: this is a blind disassembly window; literal pools/strings may appear as instructions.\n\n' \
    "$objdump" "$start" "$stop_num"
"$objdump" -D -M reg-names-std --start-address="$start_num" --stop-address="$stop_num" "$object"
