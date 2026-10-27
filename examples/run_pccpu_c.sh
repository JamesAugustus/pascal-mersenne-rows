#!/usr/bin/env bash
# Compile outside the publication folder. Requires a C compiler and GMP headers.
set -euo pipefail
example_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
build_dir=$(mktemp -d /tmp/pccpu-c.XXXXXX)
cleanup() { rm -f -- "$build_dir/pccpu_model"; rmdir -- "$build_dir"; }
finish() {
    status=$?
    cleanup
    if [[ ${1:-} == --terminal ]]; then
        printf '\nKaynak: %s/pccpu_address_model.c\n' "$example_dir"
        printf 'Cikis kodu: %s. Pencereyi kapatmak icin Enter.\n' "$status"
        read -r _ || true
    fi
    exit "$status"
}
trap 'finish "${1:-}"' EXIT
printf 'C / GMP derleniyor...\n'
"${CC:-cc}" -std=c11 -O2 -Wall -Wextra -Werror -pedantic \
    "$example_dir/pccpu_address_model.c" -lgmp -o "$build_dir/pccpu_model"
"$build_dir/pccpu_model" --test
printf '\n'
"$build_dir/pccpu_model" --demo
