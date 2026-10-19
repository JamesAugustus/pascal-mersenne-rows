"""Check Pascal row p+2 in base 2**p-1. No third-party packages.

Author: James Augustus. October 2026. License: MIT.
"""

import argparse
import sys

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
    b = (1 << p) - 1
    moduli = [(1 << 127) - 1, (1 << 89) - 1, (1 << 61) - 1]
    h = [0, 0, 0]
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
    print(line)
    return 0 if clean and value_mod and value_full else 1


if __name__ == "__main__":
    sys.exit(main())
