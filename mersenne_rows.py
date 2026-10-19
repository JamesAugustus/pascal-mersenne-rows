"""Check Pascal row p+2 in base 2**p-1. No third-party packages.

Author: James Augustus. October 2026. License: MIT.
"""

import argparse
import sys
from math import gcd

MODULI = tuple((1 << u) - 1 for u in (127, 89, 61))


def select_moduli(p, candidates):
    """Keep only coprime bases; modular powers avoid building the full base."""
    return [q for q in candidates if gcd(pow(2, p, q) - 1, q) == 1]


def exponent(text):
    if not text.isascii() or not text.isdecimal():
        raise argparse.ArgumentTypeError("p must be a decimal integer >= 2")
    try:
        p = int(text)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("p is too long") from exc
    if p < 2:
        raise argparse.ArgumentTypeError("p must be a decimal integer >= 2")
    return p


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Check Pascal row p+2 in Mersenne base 2^p-1 (default p=7)."
    )
    parser.add_argument("p", nargs="?", type=exponent, default=7, help="decimal exponent >= 2")
    parser.add_argument("mode", nargs="?", choices=("full",), help="also compare exact value")
    args = parser.parse_args(argv)
    p, full = args.p, args.mode == "full"
    n = p + 2
    e = p * n
    moduli = select_moduli(p, MODULI)
    if not moduli:
        print("p=%d row=%d clean=unchecked value(mod)=unavailable moduli=0/%d" % (p, n, len(MODULI)))
        print("No coprime check modulus; row and full checks were not run.", file=sys.stderr)
        return 1
    b = (1 << p) - 1
    h = [0] * len(moduli)
    v = 0
    clean, R, digits = True, 1, []
    for k in range(n + 1):
        if p <= 20:
            digits.append(R)
        if R >= b:
            clean = False
        h = [(x * b + R) % q for x, q in zip(h, moduli)]
        if full:
            v = v * b + R
        R = R * (n - k) // (k + 1)
    if digits:
        print(" ".join(map(str, digits)))
    value_mod = all(x == pow(2, e, q) for x, q in zip(h, moduli))
    line = "p=%d row=%d clean=%s value(mod)=%s" % (p, n, "yes" if clean else "NO", "ok" if value_mod else "WRONG")
    if full:
        value_full = v == 1 << e
        line += " value(full)=%s (%d bits)" % ("ok" if value_full else "WRONG", v.bit_length())
    else:
        value_full = True
    line += " moduli=%d/%d" % (len(moduli), len(MODULI))
    print(line)
    return 0 if clean and value_mod and value_full else 1


if __name__ == "__main__":
    sys.exit(main())
