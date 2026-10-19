# Powers of two as carry-free Pascal rows in Mersenne bases

James Augustus

## Abstract

Let M_p = 2^p − 1. We show that 2^(p·(p+2)), written in base M_p, has as its digits exactly the entries of row p + 2 of Pascal's triangle, and that no digit reaches the base for every odd p ≥ 7. The middle digit equals (p + 2) times a Catalan number, and its prime factorization follows from Legendre's formula without computing the digit itself. The statement was checked for all 52 known Mersenne prime exponents. The tools are classical; the note records a particular choice of base and row.

## 1. Setting

For any base b, (b + 1)^n = Σ_{k=0}^{n} C(n,k) b^(n−k). The coefficients are the base-b digits of (b + 1)^n if and only if every C(n,k) is less than b, that is, if the middle coefficient is less than b. In base 10 this holds for 11^n with n ≤ 4 and fails from n = 5 on.

We take b = M_p, so that b + 1 = 2^p, and n = p + 2. This is where the exponent comes from, (b + 1)^n = (2\^p)\^(p+2) = 2^(p·(p+2)). Throughout, p is odd, n = 2x + 1 and x = (p + 1)/2. The middle coefficient of row n is C(n, x) = C(n, x + 1).

[Figure 1: row coordinates (PDF)](coordinates_en.pdf)

## 2. Results

**Theorem 1.** Σ_{k=0}^{n} C(n,k) M_p^(n−k) = 2^(p·(p+2)).

**Theorem 2.** If p ≥ 7 is odd, then C(p + 2, (p + 1)/2) < M_p. Hence every entry of row p + 2 is a base-M_p digit, and 2^(p·(p+2)) is written in base M_p as that row.

**Theorem 3.** C(2x + 1, x) = (2x + 1) Cat_x, where Cat_x = C(2x, x)/(x + 1). In particular the middle digit equals (p + 2) Cat_((p+1)/2), and the second digit p + 2 divides it.

**Corollary 4.** Every prime q with (p + 3)/2 < q ≤ p + 2 divides the middle digit exactly once. If (p + 3)/2 is prime, it does not divide the middle digit.

Example, p = 7: base 127, 2^63 = 128^9 has digits 1, 9, 36, 84, 126, 126, 84, 36, 9, 1, and 126 = 9 · 14 = 9 · Cat_4. The prime 5 = (p + 3)/2 does not divide 126.

## 3. Proofs

*Theorem 1* is the binomial theorem with b = M_p.

*Theorem 2.* Induction on odd n = p + 2 ≥ 9. For n = 9, C(9, 4) = 126 < 127 = M_7. For the step,

C(2x + 3, x + 1) / C(2x + 1, x) = (2x + 3)(2x + 2) / ((x + 1)(x + 2)) = 2(2x + 3)/(x + 2) < 4.

If C(2x + 1, x) < M_p, then C(2x + 3, x + 1) < 4 M_p < 4 M_p + 3 = M_(p+2). For p = 3 and p = 5 the inequality fails (10 > 7, 35 > 31).

*Theorem 3.* C(2x + 1, x) = (2x + 1)! / (x! (x + 1)!) = (2x + 1) · (2x)! / (x! (x + 1)!) = (2x + 1) C(2x, x)/(x + 1).

*Corollary 4.* By Legendre's formula the exponent of q in C(n, x) is v_q(n!) − v_q(x!) − v_q((x + 1)!). If x + 1 < q ≤ n, then n < 2q, so v_q(n!) = 1 and the other two terms vanish. If q = x + 1, then v_q((x + 1)!) = 1 and the exponent is 0.

## 4. Computations

The middle digit was computed with GMP for all 52 known Mersenne prime exponents, p = 2, …, 136279841, and the tables were checked a second time with independent code. Selected rows:

| p | bits of middle digit | bits of M_p | decimal digits of middle digit |
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

The gap in bits is about ½ log₂ p − 2, as expected from C(2x, x) ~ 4^x / √(πx). For 7 ≤ p ≤ 37, row p + 2 is the last clean row in base M_p; from p = 38 on, row p + 3 is clean as well.

## 5. Remarks

1. Primality plays no role. The theorems hold for every odd p ≥ 7; for example M_11 = 23 · 89 gives a clean row. The Mersenne prime exponents are used only as test cases.
2. The ingredients are standard: the binomial theorem, Legendre's formula, the identity of Theorem 3, and the extension of the powers-of-11 pattern to arbitrary bases [2, 3]. I have not found the choice b = M_p, n = p + 2 in the literature, but the search was brief.
3. The digits can be produced one from the next, R_(k+1) = R_k (n − k)/(k + 1), and the value recovered by Horner's rule. No multiplication of large numbers is needed to write the row.
4. The middle digit can also be found by addition alone, without the Catalan number: each middle is the previous middle plus its neighbour, C(9, 4) = C(8, 4) + C(8, 3) = 70 + 56. My first formula contained a Catalan number; I later rewrote it in this additive form.

## 6. Code

`mersenne_rows_gmp.c` (C with GMP) prints the row, checks that every digit is below the base, and compares the value with 2^(p·(p+2)) exactly or modulo three primes:

```
cc -O2 -o mersenne_rows_gmp mersenne_rows_gmp.c -lgmp
./mersenne_rows_gmp 7 full
./mersenne_rows_gmp 132049
```

The folder `tables/` holds four tables for all 52 exponents: the theorems with their proofs, the middle digits, the middle digits of the first 50, and their factorizations. A GMP-free check for p = 7, …, 61 is test T21_mersenne_row in `journal_tests.c`, in the companion repository `ctcpu-hunter`.

## References

1. Binomial theorem. https://mathworld.wolfram.com/BinomialTheorem.html
2. L. Jiu, C. Vignat, On binomial identities in arbitrary bases, J. Integer Sequences 19 (2016). https://arxiv.org/abs/1602.04149
3. M. S. Islam et al., Generating binomial coefficients in a row of Pascal's triangle from extensions of powers of eleven, Heliyon (2022). https://arxiv.org/abs/2005.14490
4. Legendre's formula. https://en.wikipedia.org/wiki/Legendre%27s_formula
5. OEIS A001405 (central binomial coefficients), A000108 (Catalan numbers). https://oeis.org
6. GIMPS, list of known Mersenne primes. https://www.mersenne.org/primes/

Text CC BY 4.0, code MIT.
