"""Copy the bounded publication package into a selected folder using Python 3."""

import argparse
import os
from pathlib import Path
import shutil
import stat
import tempfile

FILES = (
    "CITATION.cff",
    "LICENSE",
    "README.md",
    "coordinates_en.pdf",
    "setup/install.bat",
    "setup/install.command",
    "setup/install.py",
    "mersenne_rows.py",
    "mersenne_rows_gmp.c",
    "note.md",
    "note.pdf",
    "setup/requirements.txt",
    "run.bat",
    "run.command",
    "run.sh",
    "tables/middle_digits.txt",
    "tables/middle_digits_1_to_50.txt",
    "tables/middle_digits_factored.txt",
    "tables/theorems.txt",
    "tests/test_local.py",
    "tr/README.md",
    "tr/coordinates_tr.pdf",
    "tr/note.md",
    "tr/note.pdf",
    "tr/tables/middle_digits.txt",
    "tr/tables/middle_digits_1_to_50.txt",
    "tr/tables/middle_digits_factored.txt",
    "tr/tables/theorems.txt",
)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Install the Mersenne row checker in TARGET.")
    parser.add_argument("target", type=Path, help="selected destination folder")
    parser.add_argument("--overwrite", action="store_true", help="replace conflicting managed files")
    args = parser.parse_args(argv)
    source = Path(__file__).resolve().parent.parent
    target = args.target.expanduser().resolve()

    if target == source or target in source.parents or source in target.parents:
        parser.error("target must be separate from the source folder and its parents/children")
    if target.exists() and not target.is_dir():
        parser.error(f"target is not a directory: {target}")

    # Complete the preflight before creating the destination or any files.
    directories = sorted({Path(name).parent for name in FILES if Path(name).parent != Path(".")},
                         key=lambda path: (len(path.parts), str(path)))
    for relative in directories:
        destination = target / relative
        if destination.is_symlink() or (destination.exists() and not destination.is_dir()):
            parser.error(f"destination path is not a directory: {destination}")
    changed = []
    for name in FILES:
        src, dst = source / name, target / name
        if not src.is_file() or src.is_symlink():
            parser.error(f"missing or unsafe source file: {src}")
        if dst.is_symlink() or (dst.exists() and not dst.is_file()):
            parser.error(f"destination path is not a regular file: {dst}")
        if dst.exists() and dst.read_bytes() == src.read_bytes():
            continue
        if dst.exists() and not args.overwrite:
            parser.error(f"conflicting file: {dst} (use --overwrite to replace managed files)")
        changed.append(name)

    target.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".mersenne-install-", dir=target) as temporary:
        staged = Path(temporary)
        for name in changed:
            (staged / name).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source / name, staged / name)
            if (staged / name).read_bytes() != (source / name).read_bytes():
                raise OSError(f"copy verification failed: {name}")
            if os.name == "posix" and name in ("setup/install.command", "run.command", "run.sh"):
                path = staged / name
                path.chmod(path.stat().st_mode | stat.S_IXUSR)
        for relative in directories:
            (target / relative).mkdir(exist_ok=True)
        for name in changed:
            os.replace(staged / name, target / name)
    print(f"Installed {len(changed)} file(s) in {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
