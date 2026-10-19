# Pascal Mersenne Rows

This is one of the approaches I am exploring for representing numbers
using Pascal structures. Here I write certain powers of two as Pascal
rows in Mersenne bases. The proof is in the mathematical note; Python and
C programs are included to reproduce examples.
[Türkçe](tr/README.md)

## Result and example

The note proves when the chosen base and row give a digit representation
without carrying: row p + 2 is carry-free in base 2^p − 1 for every integer p ≥ 7.

For example, these base-127 digits represent 2^63:

```text
1 9 36 84 126 126 84 36 9 1
```

Here 126 is a single digit. Every digit is below 127, so no carrying is
needed. This result is not a general primality test.

## How I did it

I used the Pascal coefficients in the binomial theorem as digits in the
chosen base. The programs compute those coefficients, check that each fits
the base, and verify that their value equals the expected power of two.
This lets you reproduce a carry-free row and inspect when its coefficients
are valid digits. The value comparison checks the implementation of an
identity already given by the binomial theorem; it is not a separate
mathematical proof or a primality test.

Formulas, proofs, and references are in the [mathematical note](note.pdf)
([text version](note.md)). The [figure](coordinates_en.pdf) explains
the positions in the row.

## How to run

Python 3 is sufficient; no third-party packages are needed. From the
repository root:

```sh
python3 mersenne_rows.py 7 full
```

On Windows use `py -3 mersenne_rows.py 7 full`. Expect `clean=yes`,
`value(mod)=ok`, and `value(full)=ok`. `clean=yes` means every coefficient
is below the base, so no carrying is needed. The reported `64 bits` is the length
of this example's result, not a fixed 64-bit limit. `moduli=3/3` means
all three candidate moduli were used; those sharing a factor with the base
are skipped. If none is usable, the program reports that the check is
unavailable.

Both programs traverse all n + 1 coefficients of row n = p + 2. The `full`
result occupies p(p + 2) + 1 bits; time and memory costs grow rapidly for
large exponents. These commands do not replace the separate programs
used to compute large central coefficients in the historical 52-exponent
tables.

## Setup and tests

Installation is optional. To copy the package into your home folder:

```sh
python3 setup/install.py "$HOME/Mersenne"
```

Windows: `setup\install.bat "%USERPROFILE%\Mersenne"`.
macOS: `./setup/install.command "$HOME/Mersenne"`.
The installer does not download Python or GMP and does not overwrite
conflicting package files automatically. Run tests with
`python3 -B tests/test_local.py`.

The optional C version needs a C compiler and GMP:

```sh
cc -O2 -o mersenne_rows_gmp mersenne_rows_gmp.c -lgmp
./mersenne_rows_gmp 7 full
```

## Files and terms

- `setup/`: installation; `tests/`: program and installation checks.
- `tables/`: tables; `coordinates_en.pdf`: figure. Turkish versions are under `tr/`.
- `note.md`, `note.pdf`: text and PDF versions of the mathematical note.
- Licenses: all source code, launchers, setup files and tests are covered by
  [MIT](LICENSE). English and Turkish documentation, PDFs, figures, tables
  and citation metadata are covered by [CC BY 4.0](LICENSE-CC-BY-4.0).
  Copyright © 2026 James Augustus. These licenses apply to their respective
  materials, rather than offering a choice of license for every file.
- [CITATION.cff](CITATION.cff): citation information.

James Augustus · jamesaugustus1313@gmail.com
