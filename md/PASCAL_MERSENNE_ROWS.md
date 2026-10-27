# Powers of two as carry-free Pascal rows in Mersenne bases

James Augustus

## Abstract

Let $M_p$ = 2<sup>p</sup> − 1. We show that $2^{p(p+2)}$, written in base $M_p$, has as its digits exactly the entries of row p + 2 of Pascal's triangle, and that no digit reaches the base for every integer p ≥ 7. For odd p, the middle digit equals (p + 2) times a Catalan number, and its prime factorization follows from Legendre's formula without computing the digit itself. The accompanying historical tables cover the 52 Mersenne prime exponents in the 14 October 2026 working list. The tools are classical; the note records a particular choice of base and row.

## 1. Setting

For any base b, $(b+1)^n=\sum_{k=0}^{n}\binom{n}{k}b^{n-k}$. The coefficients are the base-b digits of (b + 1)<sup>n</sup> if and only if every C(n,k) is less than b, that is, if the middle coefficient is less than b. In base 10 this holds for 11<sup>n</sup> with n ≤ 4 and fails from n = 5 on.

We take b = $M_p$, so that b + 1 = 2<sup>p</sup>, and n = p + 2. This is where the exponent comes from, (b + 1)<sup>n</sup> = `(2^p)^(p+2)` = $2^{p(p+2)}$. Here p is an integer with p ≥ 2. The carry-free result applies to every integer p ≥ 7. For the odd-p results in Theorem 3 and Corollary 4, write n = 2x + 1 and x = (p + 1)/2; the two middle coefficients are C(n, x) = C(n, x + 1).

[Figure 1: row coordinates (PDF)](../pdf/figures/coordinates.pdf)

## 2. Results

**Theorem 1.** $\sum_{k=0}^{n}\binom{n}{k}M_p^{n-k}=2^{p(p+2)}$.

**Theorem 2.** For every integer p ≥ 7, C(p + 2, ⌊(p + 2)/2⌋) < $M_p$. Hence every entry of row p + 2 is a base-$M_p$ digit, and $2^{p(p+2)}$ is written in base $M_p$ as that row.

**Theorem 3.** For odd p ≥ 7, let x = (p + 1)/2. Then C(2x + 1, x) = (2x + 1) $\mathrm{Cat}_x$, where $\mathrm{Cat}_x=\frac{1}{x+1}\binom{2x}{x}$. In particular the middle digit equals (p + 2) $\mathrm{Cat}_{(p+1)/2}$, and the second digit p + 2 divides it.

**Corollary 4.** For odd p ≥ 7, every prime q with (p + 3)/2 < q ≤ p + 2 divides the middle digit exactly once. If (p + 3)/2 is prime, it does not divide the middle digit.

Example, p = 7: base 127, 2<sup>63</sup> = 128<sup>9</sup> has digits 1, 9, 36, 84, 126, 126, 84, 36, 9, 1, and 126 = 9 · 14 = 9 · $\mathrm{Cat}_4$. The prime 5 = (p + 3)/2 does not divide 126.

## 3. Proofs

*Theorem 1* is the binomial theorem with b = $M_p$.

*Theorem 2.* Induct separately over odd and even p, increasing p by 2. For odd p, start at n = p + 2 = 9: C(9, 4) = 126 < 127 = M<sub>7</sub>. For the step,

$\frac{\binom{2x+3}{x+1}}{\binom{2x+1}{x}}=\frac{(2x+3)(2x+2)}{(x+1)(x+2)}=\frac{2(2x+3)}{x+2}<4$.

If C(2x + 1, x) < $M_p$, then C(2x + 3, x + 1) < 4 $M_p$ < 4 $M_p$ + 3 = $M_{p+2}$. For even p, start at p = 8: C(10, 5) = 252 < 255 = M<sub>8</sub>. Writing n = 2x, the next middle coefficient satisfies

$\frac{\binom{2x+2}{x+1}}{\binom{2x}{x}}=\frac{2(2x+1)}{x+1}<4$.

Thus the same comparison with $M_{p+2}$ = 4 $M_p$ + 3 proves the even-p step. The two inductions cover all integers p ≥ 7. For p = 2, 3, 4, 5, 6, the middle coefficients are respectively 6, 10, 20, 35, 70, exceeding the bases 3, 7, 15, 31, 63.

*Theorem 3.* $\binom{2x+1}{x}=\frac{(2x+1)!}{x!(x+1)!}=(2x+1)\frac{(2x)!}{x!(x+1)!}=\frac{2x+1}{x+1}\binom{2x}{x}$.

*Corollary 4.* By Legendre's formula the exponent of q in C(n, x) is $v_q(n!)-v_q(x!)-v_q((x+1)!)$. If x + 1 < q ≤ n, then n < 2q, so v<sub>q</sub>(n!) = 1 and the other two terms vanish. If q = x + 1, then v<sub>q</sub>((x + 1)!) = 1 and the exponent is 0.

## 4. Computations

The tables record middle-coefficient calculations for the 52 Mersenne prime exponents in the 14 October 2026 working list, p = 2, …, 136279841. They were calculated using gmpy2 and checked by a separate script that directly recomputed the middle coefficients with gmpy2.comb; its archived output reports 52 rows and no mismatches. Both calculations use the GMP backend, so this is not verification by an independent arithmetic implementation. That historical check covers the table fields and middle coefficients, not a traversal or full-value reconstruction of each Pascal row by the CLI below. Selected rows:

| p | bits of middle digit | bits of $M_p$ | decimal digits of middle digit |
|---|---|---|---|
| 7 | 7 | 7 | 3 |
| 13 | 13 | 13 | 4 |
| 31 | 31 | 31 | 10 |
| 127 | 126 | 127 | 38 |
| 521 | 519 | 521 | 156 |
| 1279 | 1276 | 1279 | 384 |
| 132049 | 132043 | 132049 | 39749 |
| 82589933 | 82589922 | 82589933 | 24862044 |
| 136279841 | 136279830 | 136279841 | 41024317 |

With h(p) = $\frac12\log_2(\pi p/2)$, the logarithmic gap is asymptotic to h(p) − 2. Actual integer bit lengths also involve rounding. For 7 ≤ p ≤ 37, row p + 2 is the last clean row in base $M_p$; from p = 38 on, row p + 3 is clean as well.

## 5. Remarks

1. Primality plays no role. The carry-free row result holds for every integer p ≥ 7; Theorem 3 and Corollary 4 retain the odd-p assumption; for example M<sub>11</sub> = 23 · 89 gives a clean row. The Mersenne prime exponents are used only as test cases.
2. The ingredients are standard: the binomial theorem, Legendre's formula, the identity of Theorem 3, and the extension of the powers-of-11 pattern to arbitrary bases [2, 3]. I have not found the choice b = $M_p$, n = p + 2 in the literature, but the search was brief.
3. The digits can be produced one from the next, $R_{k+1}=R_k\frac{n-k}{k+1}$, and the value recovered by Horner's rule. This recurrence multiplies a growing coefficient by an integer no larger than n and performs an exact division; these operations have a cost. Recovering the full value with Horner additionally requires large-integer multiplications.
4. The middle digit can also be found by addition alone, without the Catalan number: each middle is the previous middle plus its neighbour, C(9, 4) = C(8, 4) + C(8, 3) = 70 + 56. My first formula contained a Catalan number; I later rewrote it in this additive form.

## 6. Code

`mersenne_rows.py` and `mersenne_rows_gmp.c` (C with GMP) generate the coefficients and report whether each is below the base as `clean`. They print the row only for p ≤ 20. They compare the value with $2^{p(p+2)}$ modulo those of three candidate primes that are coprime to the base; `moduli=m/3` reports the number used. Moduli sharing a factor with the base are skipped to avoid a vacuous check. If none remains, the programs report `value(mod)=unavailable`, `clean=unchecked` and exit with status 1 without calculating the row or full value. The `full` option also compares the exact integers.

The value checks test implementation consistency with the binomial identity; they are not an independent mathematical proof or a primality test. The substantive representation condition is that the largest coefficient is below the base. Both programs traverse n + 1 coefficients; suppressing row output does not remove that work. The `full` result has p(p + 2) + 1 bits. For very large exponents, this traversal and full-value storage may be impractical; directly computing the middle coefficient is a different task.

```
cc -O2 -o mersenne_rows_gmp mersenne_rows_gmp.c -lgmp
./mersenne_rows_gmp 7 full
./mersenne_rows_gmp 132049
```

The folder `tables/` holds four tables from the 52-exponent study: the theorems with their proofs, the middle digits, the middle digits of the first 50, and their factorizations. A GMP-free check for p = 7, …, 61 is test T21<sub>m</sub>ersenne<sub>r</sub>ow in `journal_tests.c`, in the companion repository `ctcpu-hunter`.

## References

1. Binomial theorem. https://mathworld.wolfram.com/BinomialTheorem.html
2. L. Jiu, C. Vignat, On binomial identities in arbitrary bases, J. Integer Sequences 19 (2016). https://arxiv.org/abs/1602.04149
3. M. S. Islam et al., Generating binomial coefficients in a row of Pascal's triangle from extensions of powers of eleven, Heliyon (2022). https://arxiv.org/abs/2005.14490
4. Legendre's formula. https://en.wikipedia.org/wiki/Legendre%27s<sub>f</sub>ormula
5. OEIS A001405 (central binomial coefficients), A000108 (Catalan numbers). https://oeis.org
6. GIMPS, list of known Mersenne primes. https://www.mersenne.org/primes/

Text CC BY 4.0, code MIT.
