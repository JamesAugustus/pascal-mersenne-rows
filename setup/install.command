#!/bin/sh
script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd) || exit 2
exec python3 "$script_dir/install.py" "$@"
