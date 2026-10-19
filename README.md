# Pascal Mersenne Rows

This is one of the approaches I am exploring for representing numbers
using Pascal structures. Here I write certain powers of two as Pascal
rows in Mersenne bases. The proof is in the mathematical note; Python and
C programs are included to reproduce examples.
[Türkçe](tr/README.md)

## Result and example

The note proves when the chosen base and row give a digit representation
without carrying.

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
`value(mod)=ok`, and `value(full)=ok`. The reported `64 bits` is the length
of this example's result, not a limit on the program's number size.

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
- [LICENSE](LICENSE): text and tables CC BY 4.0; code MIT.
- [CITATION.cff](CITATION.cff): citation information.

James Augustus · jamesaugustus1313@gmail.com
