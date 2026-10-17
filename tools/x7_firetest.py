#!/usr/bin/env python3
"""Read-only reconnaissance harness for X7-MiyooCFW. Python 3.9+."""
import argparse
import hashlib
import os
import re
import shutil
import subprocess
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path

VERSION = "0.1.0"
EXEC_EXT = {".axf", ".elf", ".drv", ".plg", ".mod"}
TEXT_EXT = {".fex", ".ini", ".cfg", ".conf", ".desktop", ".reg", ".txt", ".xml"}
PAYLOAD_PREFIXES = ("apps__", "drv__", "mod__", "cedar__")
SIGNALS = re.compile(
    r"(linux version|u-boot|uboot|bootargs|root=/dev|/proc/|/sys/|/dev/fb|"
    r"framebuffer|buildroot|busybox|glibc|uclibc|musl|libc\.so|"
    r"application://|game_[a-z0-9_]+|\.axf|lcd|display|disp|audio|sound|"
    r"alsa|oss|key|button|gpio|mmc|sdio|usb|dram|lcd0_para|HSD045F8W7|"
    r"9806E|ATJ227|ATS3603|actions semiconductor|SPIWRITE|SPI_WriteComm|"
    r"b:\\|d:\\|setenv|console=tty|kernel|initrd|ramdisk)",
    re.IGNORECASE,
)

def run_cmd(argv, timeout=15):
    try:
        p = subprocess.run(argv, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                           text=True, errors="replace", timeout=timeout, check=False)
        return p.returncode, p.stdout.rstrip()
    except FileNotFoundError:
        return 127, "[not installed] " + argv[0]
    except subprocess.TimeoutExpired as e:
        return 124, "[timeout after %ss] %s" % (timeout, e.stdout or "")
    except Exception as e:
        return 125, "[error] %s: %s" % (type(e).__name__, e)

def command_text(argv, timeout=15):
    code, output = run_cmd(argv, timeout)
    return "$ " + " ".join(map(str, argv)) + "\n[exit=%s]\n%s" % (code, output)

def safe_inside(child, parent):
    try:
        child.resolve().relative_to(parent.resolve())
        return True
    except (ValueError, OSError):
        return False

def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()

def save(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8", errors="replace")

def inventory(roots):
    records = []
    for root in roots:
        if not root.is_dir():
            continue
        for path in root.rglob("*"):
            if path.is_file():
                try:
                    records.append((path, path.stat().st_size, path.suffix.lower()))
                except OSError:
                    pass
    return records

def main():
    parser = argparse.ArgumentParser(description="Read-only X7 firmware reconnaissance")
    parser.add_argument("--project", default=str(Path.home() / "X7-FirmwareLab"))
    parser.add_argument("--miyoo", default=None, help="Local MiyooCFW checkout")
    parser.add_argument("--volume", default="/run/media/joshua/3EDF-BD13",
                        help="Observed PC-visible game-storage mount")
    parser.add_argument("--image", default=None, help="Original image, inspected read-only")
    parser.add_argument("--hash-image", action="store_true",
                        help="Hash the entire image; multi-GB read")
    parser.add_argument("--output", default=None)
    parser.add_argument("--max-binaries", type=int, default=160)
    args = parser.parse_args()

    project = Path(args.project).expanduser().resolve()
    volume = Path(args.volume).expanduser().resolve() if args.volume else None
    miyoo = Path(args.miyoo).expanduser().resolve() if args.miyoo else project / "MiyooCFW"
    timestamp = datetime.now().astimezone().strftime("%Y%m%d-%H%M%S%z")
    output = Path(args.output).expanduser().resolve() if args.output else (
        project / "reports" / "fire-tests" / timestamp)
    if volume and volume.exists() and safe_inside(output, volume):
        print("ERROR: output directory is inside the observed volume. Refusing.", file=sys.stderr)
        return 2
    output.mkdir(parents=True, exist_ok=True)

    env = [
        "X7-MiyooCFW read-only fire-test report",
        "Script version: " + VERSION,
        "Timestamp: " + datetime.now().astimezone().isoformat(),
        "Python: " + sys.version.replace(os.linesep, " "),
        "Host: %s %s %s" % (os.uname().sysname, os.uname().release, os.uname().machine),
        "Project exists: %s (%s)" % (project.exists(), project),
        "Volume exists: %s (%s)" % (bool(volume and volume.exists()), volume),
        "Miyoo checkout exists: %s (%s)" % (miyoo.exists(), miyoo),
        "Output: " + str(output),
        "",
        "Tool availability:"
    ]
    for name in ("file", "readelf", "objdump", "strings", "rizin", "rz-bin",
                 "lsblk", "findmnt", "df", "lsusb", "journalctl", "fdisk", "parted", "git"):
        env.append("- %s: %s" % (name, shutil.which(name) or "not found"))
    save(output / "00-environment.txt", "\n".join(env))

    host = [
        command_text(["uname", "-a"]),
        command_text(["lsblk", "-o",
            "NAME,PATH,SIZE,TYPE,FSTYPE,LABEL,UUID,RO,RM,TRAN,MODEL,MOUNTPOINTS"]),
        command_text(["lsusb"]),
        command_text(["lsusb", "-t"]),
        "# Host kernel log only; this is not the handheld boot log.",
        command_text(["journalctl", "-k", "-b", "--no-pager", "-n", "250"], 12)
    ]
    if volume and volume.exists():
        host.insert(1, command_text(["findmnt", "-T", str(volume), "-o",
                                     "SOURCE,FSTYPE,OPTIONS,TARGET"]))
        host.insert(2, command_text(["df", "-hT", str(volume)]))
    else:
        host.insert(1, "Configured volume not found: " + str(volume))
    save(output / "01-host-and-usb.txt", "\n\n".join(host))

    miyoo_report = []
    if miyoo.exists():
        miyoo_report.append("Local MiyooCFW path: " + str(miyoo))
        for cmd in (
            ["git", "-C", str(miyoo), "branch", "--show-current"],
            ["git", "-C", str(miyoo), "rev-parse", "HEAD"],
            ["git", "-C", str(miyoo), "status", "--short"],
            ["git", "-C", str(miyoo), "submodule", "status"],
        ):
            miyoo_report.append(command_text(cmd))
        for name in (".gitmodules", "README.md", "Dockerfile-musl", "Dockerfile-uclibc"):
            path = miyoo / name
            if path.is_file():
                miyoo_report.append("\n--- " + name + " ---\n" +
                                    path.read_text(errors="replace")[:14000])
    else:
        miyoo_report.append("Miyoo checkout not found. Pass --miyoo PATH.")
    save(output / "02-miyoo-checkout.txt", "\n\n".join(miyoo_report))

    roots = [project / "extracted" / "original-fat16",
             project / "extracted" / "bulk-decoded"]
    files = inventory(roots)
    counts = Counter(ext or "[no extension]" for _, _, ext in files)
    inv = ["path relative to project\tbytes\textension"]
    for path, size, ext in sorted(files, key=lambda r: str(r[0]).lower()):
        try:
            relative = str(path.relative_to(project))
        except ValueError:
            relative = str(path)
        inv.append("%s\t%s\t%s" % (relative, size, ext))
    save(output / "03-firmware-inventory.tsv",
         "Total files: %s\nExtension counts: %s\n\n%s" % (
             len(files), ", ".join("%s=%s" % pair for pair in counts.most_common()),
             "\n".join(inv)))

    def is_binary_candidate(path):
        name = path.name.lower()
        key_files = {"epos.img", "app_config.bin", "theme.bin", "lang.bin",
                     "key_ref.dat", "secret.bin"}
        if path.suffix.lower() in EXEC_EXT:
            return True
        if name in key_files:
            return True
        return path.suffix.lower() == ".bin" and name.startswith(PAYLOAD_PREFIXES)

    binaries = [(p, size) for p, size, ext in files
                if is_binary_candidate(p) and size <= 128 * 1024 * 1024]
    binaries.sort(key=lambda item: (0 if item[0].suffix.lower() in EXEC_EXT else 1,
                                   str(item[0]).lower()))
    binaries = binaries[:max(1, args.max_binaries)]
    signature_report, elf_report, strings_report = [], [], []
    for path, size in binaries:
        rel = str(path.relative_to(project)) if safe_inside(path, project) else str(path)
        try:
            with path.open("rb") as stream:
                header = stream.read(64)
            signature_report.append("--- %s (%s bytes) ---\nhex=%s\nascii=%s" % (
                rel, size, header.hex(" "),
                "".join(chr(c) if 32 <= c < 127 else "." for c in header)))
        except OSError as error:
            signature_report.append("%s: READ ERROR %s" % (rel, error))
            continue
        elf_report.append("--- %s (%s bytes) ---" % (rel, size))
        elf_report.append(command_text(["file", str(path)]))
        if shutil.which("readelf") and (
            path.suffix.lower() in EXEC_EXT or header[:4] == b"\x7fELF"
        ):
            elf_report.append(command_text(
                ["readelf", "-h", "-l", "-S", "-A", str(path)], 12))
        try:
            elf_report.append("sha256=" + sha256(path))
        except OSError as error:
            elf_report.append("SHA256 ERROR: " + str(error))
        if shutil.which("strings"):
            code, raw = run_cmd(["strings", "-a", "-n", "5", str(path)], 20)
            matches = [line for line in raw.splitlines() if SIGNALS.search(line)]
            if matches:
                strings_report.append("--- %s (strings exit %s) ---" % (rel, code))
                strings_report.extend(matches[:220])
                if len(matches) > 220:
                    strings_report.append("[truncated %s additional matches]" % (len(matches)-220))
    save(output / "04-binary-signatures.txt",
         "\n\n".join(signature_report) or "No candidates found.")
    save(output / "05-executable-analysis.txt",
         "\n".join(elf_report) or "No candidate executable artifacts found.")
    save(output / "06-interesting-strings.txt",
         "\n".join(strings_report) or "No matching strings or strings utility unavailable.")

    cfg_report, configs = [], []
    for root in roots:
        if root.is_dir():
            configs.extend(root.rglob("app_config.fex"))
    for path in sorted(set(configs)):
        cfg_report.append("--- %s ---" % path)
        content = path.read_text(errors="replace")
        parts = re.split(r"(?m)^\s*(\[[^\]]+\])\s*$", content)
        for index in range(1, len(parts), 2):
            header = parts[index]
            body = parts[index+1] if index+1 < len(parts) else ""
            if re.search(r"lcd|display|dram|boot|uart|serial|usb|audio|sound|key|gpio|power|mmc|sd",
                         header, re.I):
                cfg_report.extend([header, body.strip()[:10000]])
        globals_text = parts[0] if parts else ""
        global_hits = [line for line in globals_text.splitlines()
                       if SIGNALS.search(line)]
        if global_hits:
            cfg_report.extend(["[GLOBAL RELEVANT LINES]"] + global_hits[:150])
    for root in roots:
        if not root.is_dir():
            continue
        for path in root.rglob("*"):
            if not path.is_file() or path.suffix.lower() not in TEXT_EXT:
                continue
            if path.name.lower() == "app_config.fex":
                continue
            try:
                if path.stat().st_size > 512 * 1024:
                    continue
                lines = path.read_text(errors="replace").splitlines()
            except OSError:
                continue
            matches = [line for line in lines if SIGNALS.search(line)]
            if matches and path.suffix.lower() in {".desktop", ".ini", ".cfg", ".conf", ".fex"}:
                cfg_report.append("--- %s ---" % path)
                cfg_report.extend(matches[:120])
    save(output / "07-config-and-launch-paths.txt",
         "\n".join(cfg_report) or "No high-signal configuration found.")

    storage = []
    if volume and volume.is_dir():
        storage.append(command_text(["findmnt", "-T", str(volume), "-o",
                                     "SOURCE,FSTYPE,OPTIONS,TARGET"]))
        storage.append("Top-level entries:")
        for path in sorted(volume.iterdir(), key=lambda p: p.name.lower()):
            try:
                kind = "dir" if path.is_dir() else "file"
                size = path.stat().st_size if path.is_file() else "-"
                storage.append("%s\t%s\t%s" % (kind, size, path.name))
            except OSError:
                pass
        memory_dir = volume / "GAME_MEMORY"
        if memory_dir.is_dir():
            storage.append("\n=== GAME_MEMORY files ===")
            for path in sorted(memory_dir.glob("*"), key=lambda p: p.name.lower()):
                if not path.is_file():
                    continue
                try:
                    with path.open("rb") as stream:
                        data = stream.read(256)
                    storage.append("--- %s size=%s ---\nhex=%s\nascii=%s" % (
                        path.name, path.stat().st_size, data.hex(" "),
                        "".join(chr(c) if 32 <= c < 127 else "." for c in data)))
                except OSError as error:
                    storage.append("%s: %s" % (path.name, error))
        mame = volume / "GAME" / "MAME"
        if mame.is_dir():
            packages = sorted((p for p in mame.rglob("*.kg") if p.is_file()),
                              key=lambda p: p.stat().st_size)
            sample = (packages[:3] + packages[max(0, len(packages)//2-1):len(packages)//2+2]
                      + packages[-3:]) if packages else []
            unique = list(dict.fromkeys(sample))
            storage.append("\n=== Representative GAME/MAME .kg headers only ===")
            for path in unique:
                try:
                    with path.open("rb") as stream:
                        header = stream.read(128)
                    storage.append("--- %s size=%s ---\n%s\nhex=%s\nascii=%s" % (
                        path.relative_to(volume), path.stat().st_size,
                        run_cmd(["file", str(path)])[1], header.hex(" "),
                        "".join(chr(c) if 32 <= c < 127 else "." for c in header)))
                except OSError as error:
                    storage.append("%s: %s" % (path, error))
    else:
        storage.append("Volume unavailable: " + str(volume))
    save(output / "08-volume-and-kg.txt", "\n".join(storage))

    image_report = []
    if args.image:
        image = Path(args.image).expanduser().resolve()
        image_report.append("Image path: " + str(image))
        if image.is_file():
            stat = image.stat()
            image_report.append("Size: %s bytes" % stat.st_size)
            image_report.append("Modified: " + datetime.fromtimestamp(stat.st_mtime).astimezone().isoformat())
            image_report.append(command_text(["file", str(image)]))
            image_report.append(command_text(["fdisk", "-l", str(image)], 20))
            with image.open("rb") as stream:
                image_report.append("First 512 bytes: " + stream.read(512).hex(" "))
            image_report.append("SHA-256: " + sha256(image) if args.hash_image
                                else "SHA-256 skipped; add --hash-image for a full read")
        else:
            image_report.append("Image path not found.")
    else:
        image_report.append("No --image supplied; skipped.")
    save(output / "09-image-check.txt", "\n".join(image_report))

    summary = [
        "# X7-MiyooCFW fire-test summary", "",
        "Timestamp: " + datetime.now().astimezone().isoformat(),
        "Script version: " + VERSION,
        "Firmware files inventoried: %s" % len(files),
        "Executable-like artifacts examined: %s" % len(binaries),
        "Volume available: %s" % bool(volume and volume.is_dir()),
        "MiyooCFW checkout found: %s" % miyoo.exists(), "",
        "## Review in this order",
        "1. 05-executable-analysis.txt: ELF class, architecture, ABI, load segments and hashes.",
        "2. 06-interesting-strings.txt: runtime, application launch, display/audio/input clues.",
        "3. 07-config-and-launch-paths.txt: LCD settings and emulator launch paths.",
        "4. 02-miyoo-checkout.txt: MiyooCFW build system and submodule state.",
        "5. 08-volume-and-kg.txt: metadata and representative file headers only.", "",
        "## Constraints",
        "- The script does not modify or flash the target volume.",
        "- Host kernel logs describe the PC, not the handheld boot process.",
        "- ARM/ELF metadata alone does not prove Linux or MiyooCFW compatibility.",
        "- Review and redact local paths and device metadata before publishing reports.", "",
        "## File extension counts",
    ] + ["- %s: %s" % pair for pair in counts.most_common()]
    save(output / "SUMMARY.md", "\n".join(summary))
    print("Collection finished. Report directory: " + str(output))
    print("Start with: " + str(output / "SUMMARY.md"))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
