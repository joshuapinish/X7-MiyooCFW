#!/usr/bin/env python3
"""Find raw payload offsets and literal absolute-pointer references to display strings."""
import argparse
import struct
from pathlib import Path

NEEDLES = [
    b"LCD_HSD045F8W7_9806E__4_5",
    b"lcd0_para",
    b"lcd_bl_en_used",
    b"lcd_pwm_used",
    b"SPI_WriteComm = 1",
    b"lcdclk",
    b"lcdde",
    b"lcdhsync",
    b"lcdvsync",
]

def all_offsets(data: bytes, needle: bytes):
    start = 0
    while True:
        offset = data.find(needle, start)
        if offset < 0:
            return
        yield offset
        start = offset + 1

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("payload", type=Path, help="decoded display.drv payload")
    parser.add_argument("--base", default="0xe0300000",
                        help="payload load address (default: 0xe0300000)")
    args = parser.parse_args()
    base = int(args.base, 0)
    data = args.payload.read_bytes()
    if not data:
        parser.error("payload is empty")

    print(f"Payload: {args.payload}")
    print(f"Bytes:   {len(data)} (0x{len(data):x})")
    print(f"Base:    0x{base:08x}")
    print("Note: pointer matches are literal little-endian absolute-address candidates, not guaranteed code xrefs.")
    found_any = False

    for needle in NEEDLES:
        offsets = list(all_offsets(data, needle))
        if not offsets:
            continue
        found_any = True
        print(f"\nSTRING {needle.decode('ascii')!r}")
        for offset in offsets:
            address = base + offset
            packed = struct.pack("<I", address & 0xffffffff)
            refs = list(all_offsets(data, packed))
            print(f"  string offset 0x{offset:06x} -> VA 0x{address:08x}")
            if not refs:
                print("    no literal 32-bit pointer to this exact address found")
                continue
            for ref in refs:
                ref_address = base + ref
                before = max(0, ref - 8)
                after = min(len(data), ref + 12)
                context = data[before:after].hex(" ")
                print(f"    pointer bytes at offset 0x{ref:06x} (VA 0x{ref_address:08x}); context: {context}")

    if not found_any:
        print("No target strings found.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
