# N(p): The Carry-Free Representation Bound for Pascal Rows

James Augustus

## Abstract

Let M_p = 2^p − 1 and let N(p) be the largest n for which every entry of row n of Pascal's triangle is below M_p, so that (M_p + 1)^n = 2^(pn) is written in base M_p as that row. I show that N(p) − p is determined exactly by a sequence of thresholds p_k = 2m_k − k − 1, where m_k is the least m with 2^k C(2m, m) < 4^m. From Robbins' bounds for Stirling's formula, N(p) = p + ½ log₂(πp/2) + E(p) with −1 < E(p) ≤ 2 − ½ log₂(7π/2) < 0.270575 for every p ≥ 7. The exact endpoints are sharp. The thresholds satisfy p_k = (2/π)4^k − k + O(1), their consecutive ratios exceed 4 and tend to 4, and every threshold row is odd. The tools are classical. Novelty in the literature has not been verified.

## 1. Setting

Throughout, p is an integer with p ≥ 2, so M_p is a valid positional base. Primality of p or M_p is not required. Write c(n) = C(n, ⌊n/2⌋) for the largest entry of row n. For any base b, (b + 1)^n = Σ_{k=0}^{n} C(n,k) b^k, and the coefficients are the base-b digits of (b + 1)^n if and only if c(n) < b. I fix b = M_p and let the row vary:

N(p) = max{ n : c(n) < M_p },  D(p) = N(p) − p,  h(p) = ½ log₂(πp/2).

Lemma 1 below shows that the clean rows form an initial segment {0, 1, …, N(p)}, so N(p) is found by stopping at the first row that fails. I also use

w(m) = 4^m / C(2m, m) (m ≥ 1),  m_k = min{ m : 2^k C(2m, m) < 4^m },  p_k = 2m_k − k − 1.

## Worked examples: what is N(p) useful for?

N(p) gives the validity boundary when Pascal coefficients are used as the digits of a number. With the base fixed, it tells us how far we can go through the rows. In the reverse direction, it helps select a sufficient base for a desired row. The examples below illustrate these uses. They are not new speed or compression results.

### Example 1. A number small enough to check by hand

For p = 3 the base is 7. Pascal row 4 is [1, 4, 6, 4, 1]. Its largest coefficient is 6 < 7, so all entries are valid digits. Indeed,

1 × 7⁴ + 4 × 7³ + 6 × 7² + 4 × 7 + 1 = 4096 = 8⁴ = 2¹².

Row 5 is [1, 5, 10, 10, 5, 1]. The value 10 is not a base-7 digit. The coefficient expansion still equals 8⁵ = 32768, but the actual digits are [1, 6, 4, 3, 5, 1]. The right-hand 10 gives remainder 3 and carry 1. The next 10 becomes 11 after that carry, giving remainder 4 and carry 1. Its neighboring 5 becomes 6. Thus N(3) = 4. This p = 3 example illustrates the definition; it is outside Theorem A, which requires p ≥ 7.

### Example 2. Equality at the boundary also fails

For p = 2 the base is 3. Row 2, [1, 2, 1], fits. Row 3, [1, 3, 3, 1], does not, because the only valid digits are 0, 1 and 2. Hence N(2) = 2. The check must be c(n) < b, not c(n) ≤ b. A program accepting equality would produce an invalid digit sequence.

### Example 3. Seeing the complete row in base 127

For p = 7 the base is 127. Row 9 is [1, 9, 36, 84, 126, 126, 84, 36, 9, 1] and represents 2⁶³. Its central coefficient is 126 < 127; the next row has central coefficient 252. Therefore N(7) = 9. In this example the first note's choice p + 2 reaches the boundary exactly.

### Example 4. Going beyond the guaranteed row

For p = 38 the situation is different:

| Row | Central coefficient | Comparison with base 274877906943 |
|---|---|---|
| 40 | 137846528820 | Smaller, coefficients remain digits |
| 41 | 269128937220 | Smaller, coefficients remain digits |
| 42 | 538257874440 | Larger, carrying is required |

N(38) = 41. Thus p + 2 = 40 is a safe choice, but not the last valid choice. A converter can accept row 41 in this base; it cannot accept the coefficients of row 42 directly as digits.

### Example 5. Choosing a base for a desired row

Suppose we want to write row 42 without carrying. Its central coefficient is 538257874440. The p = 38 base is insufficient. For p = 39 the base is 549755813887, larger than the central coefficient. Therefore 39 is the smallest sufficient p among Mersenne bases. The next central coefficient, 1052049481860, also confirms N(39) = 42.

The general decision rule is to choose the smallest p ≥ 2 satisfying c(n) < 2^p − 1 for the desired row n. This reverses the question of finding N(p) for a fixed p. It is sufficient to check the largest coefficient rather than every entry separately.

### Example 6. A number longer than one million bits

For p = 1000 the base is b = 2¹⁰⁰⁰ − 1 and the last row is N(1000) = 1005. The beginning and end of that row are

[1, 1005, 504510, …, 504510, 1005, 1].

There are 1006 digits in total. The … represents 1000 omitted Pascal coefficients, not zeros. The largest coefficient has 301 decimal digits. All coefficients are below the base. With their positional weights, these digits represent 2<sup>1 005 000</sup>.

In binary, this number is a single 1 followed by 1 005 000 zeros. Its exact binary length is therefore 1 005 001 bits. The use here is to know precisely which Pascal row represents a large number without carrying. There is no need to print its entire decimal expansion.

Using 1006 digits does not by itself compress data. Each digit may require up to 1000 bits. The number of digits and the number of bits required to store them are different quantities.

### Example 7. A number whose raw binary form needs about 125 GB

Choose p = 1 000 000. Since the thresholds give 667533 ≤ p < 2670166, we have N(p) − p = 10 and N(p) = 1 000 010. The base is b = 2<sup>1 000 000</sup> − 1.

[1, 1000010, 500009500045, …, 500009500045, 1000010, 1].

The row contains 1 000 011 digits. The omitted middle contains 1 000 005 coefficients. The represented number is 2<sup>1 000 010 000 000</sup>, with exact binary length 1 000 010 000 001 bits.

Storing those bits without compression in eight-bit bytes requires 125 001 250 001 bytes, about 125 GB. By contrast, “2 raised to 1 000 010 000 000” is a short symbolic description. A symbolic description and expanding every bit in memory are different operations. This example does not generate the entire huge number or row. The last row is determined from the mathematical threshold result.

### Example 8. A parameter of one trillion

Let p = 10¹² = 1 000 000 000 000. At this scale we can use the proved error band instead of trying every row. For h(p) = ½ log₂(πp/2), we have 20.257 < h(p) < 20.258. Combining this with −1 < E(p) ≤ 0.270575 from the mathematical note gives

19.257 < N(p) − p < 20.529.

N(p) − p is an integer. The only integer in this interval is 20. Therefore N(p) = 10¹² + 20 = 1 000 000 000 020.

Writing n = 10¹² + 20, the row has the form [1, n, n(n − 1)/2, …, n(n − 1)/2, n, 1]. There are 10¹² + 21 digits. The represented number is 2<sup>10²⁴ + 20 × 10¹²</sup>. This does not mean every coefficient was computed individually. The last row was determined by selecting the unique integer permitted by the proved bound.

### Example 9. When p itself has 101 decimal digits

Now let p = 10¹⁰⁰. In decimal, this is a single 1 followed by 100 zeros. The base is b = 2<sup>10¹⁰⁰</sup> − 1. We have 166.422 < h(p) < 166.423. The same error band gives

165.422 < N(p) − p < 166.694.

The only possible integer is 166. Therefore N(10¹⁰⁰) = 10¹⁰⁰ + 166 is determined exactly.

With n = 10¹⁰⁰ + 166, this enormous row again has the form

[1, n, n(n − 1)/2, …, n(n − 1)/2, n, 1].

Its exact digit count is 10¹⁰⁰ + 167. It represents 2<sup>10²⁰⁰ + 166 × 10¹⁰⁰</sup>. The 1 at each end is an endpoint of the Pascal row. The … stands for specific omitted binomial coefficients of row n, not unknown or arbitrary values.

The use of N(p) is especially clear here: mathematics determines the carry-free boundary for a family of rows that cannot be printed in full. This does not claim that we stored the complete row or computed and displayed every entry.

### Example 10. Boundary pairs for checking a program

| p | N(p) | First row that is not carry-free |
|---|---|---|
| 2 | 2 | 3 |
| 3 | 4 | 5 |
| 4 | 5 | 6 |
| 7 | 9 | 10 |
| 8 | 10 | 11 |
| 37 | 39 | 40 |
| 38 | 41 | 42 |
| 39 | 42 | 43 |
| 100 | 103 | 104 |
| 158 | 161 | 162 |
| 159 | 163 | 164 |
| 1000 | 1005 | 1006 |

Each table entry supplies two checks: row N(p) must fit, while row N(p) + 1 must not. These pairs can be used to check boundary handling in a base converter or a program that uses Pascal coefficients as digits. Changing p also changes the base. Jumps in this table do not mean that a row is skipped within one fixed base.

### Scope of the uses

N(p) is a mathematical tool defining the exact valid range of this representation. It can illustrate carrying in teaching, guide base selection in an algorithm, and supply boundary checks. By itself, it does not show that generating a complete Pascal row or a very large power is faster. It does not provide a separate encryption method, a general compression result, or a primality test. The cost of computing N(p) also depends on the method used.

## 2. Results

**Theorem A.** For every integer p ≥ 7, N(p) ≥ p + 2.

This is Theorem 2 of the note on powers of two as carry-free Pascal rows [1].

**Theorem B1 (characterization).** For every p ≥ 7 and every k ≥ 2, N(p) − p ≥ k if and only if p ≥ p_k. Hence N(p) − p = max{ k : p_k ≤ p }. It never decreases in p and increases by exactly 1 at each p_k.

| k | m_k | p_k |
|---|---|---|
| 2 | 5 | 7 |
| 3 | 21 | 38 |
| 4 | 82 | 159 |
| 5 | 326 | 646 |
| 6 | 1304 | 2601 |
| 7 | 5215 | 10422 |
| 8 | 20861 | 41713 |
| 9 | 83443 | 166876 |
| 10 | 333772 | 667533 |
| 11 | 1335089 | 2670166 |
| 12 | 5340354 | 10680695 |

So N(p) − p is 2 for 7 ≤ p ≤ 37, 3 for 38 ≤ p ≤ 158, 4 for 159 ≤ p ≤ 645, 5 for 646 ≤ p ≤ 2600, 6 for 2601 ≤ p ≤ 10421, and 7 from p = 10422 to p = 41712.

**Theorem B2 (thresholds).** For every k ≥ 2,

4^k/π − 1/4 − 0.07/m_k < m_k < 4^k/π + 3/4 + 1/(36(m_k − 1)).

Hence p_k = (2/π)4^k − k − 3/2 + 2φ_k with −0.07/m_k < φ_k < 1 + 1/(36(m_k − 1)), and in particular

2×4^k/π − k − 1.53 < p_k < 2×4^k/π.

For 1 ≤ k ≤ 12, m_k = ⌈4^k/π − 1/4⌉, so p_k = 2⌈4^k/π − 1/4⌉ − k − 1 and, for 7 ≤ p ≤ 42 700 000, N(p) − p = max{ k ≤ 12 : 2⌈4^k/π − 1/4⌉ − k − 1 ≤ p }.

**Theorem B3 (error band).** For every p ≥ 7,

h(p) − 1 < N(p) − p ≤ h(p) + E_max,

E_max = 2 − h(7) = 0.270574474235… < 0.270575.

The exact upper value E_max is attained only at p = 7. The decimal 0.270575 is an outward rounding, not an attained endpoint. The lower value −1 is never attained but is approached arbitrarily closely. If N(p) − p = k ≥ 3, the upper bound improves to

N(p) − p − h(p) < e(k) = −½ log₂(1 − (π/2)(k + 1.53)/4^k),

with e(3) < 0.0851, e(4) < 0.0250, e(5) < 0.0073, e(6) < 0.0021, e(7) < 0.00060. In integer form, N(p) − p = ⌊h(p)⌋ + 1 if p_k ≤ p < 2×4^k/π for some k, and N(p) − p = ⌊h(p)⌋ otherwise. Each such window contains between k and k + 2 integers: 7-10, 38-40, 159-162, 646-651, 2601-2607, 10422-10430.

**Theorem B4 (ratios).** For every k ≥ 2, 3k − 5 < p_(k+1) − 4p_k < 3k + 6. Hence p_(k+1)/p_k > 4 and p_(k+1)/p_k → 4, with p_(k+1)/p_k − 4 ≈ 3πk/(2×4^k).

| p_k | p_(k+1) | p_(k+1) − 4p_k | p_(k+1)/p_k |
|---|---|---|---|
| 38 | 159 | 7 | 4.184210 |
| 159 | 646 | 10 | 4.062893 |
| 646 | 2601 | 17 | 4.026315 |
| 2601 | 10422 | 18 | 4.006920 |
| 10422 | 41713 | 25 | 4.002398 |
| 41713 | 166876 | 24 | 4.000575 |
| 166876 | 667533 | 29 | 4.000173 |
| 667533 | 2670166 | 34 | 4.000050 |
| 2670166 | 10680695 | 31 | 4.000011 |

**Theorem C (threshold rows).** Let k ≥ 3, p = p_k and N = N(p). Then N = 2m_k − 1 is odd and

1 − 1/(N + 1) ≤ c(N)/2^p < c(N)/M_p < 1.

For example c(N)/M_p is 0.979085 at p = 38 (N = 41), 0.995350 at p = 159, 0.999538 at p = 646, 0.999826 at p = 2601 and 0.999994 at p = 10422.

## 3. Lemmas

**Lemma 1 (monotonicity).** c(0) = c(1) = 1, and c(n + 1) > c(n) for every n ≥ 1. Moreover c(n + 1) ≤ 2c(n) for all n, with c(n + 1) = 2c(n) exactly when n is odd.

*Proof.* For n = 2x, c(2x + 1)/c(2x) = (2x + 1)/(x + 1), which lies in [1, 2) and equals 1 only at x = 0. For n = 2x + 1, Pascal's rule and symmetry give c(2x + 2) = C(2x + 1, x) + C(2x + 1, x + 1) = 2c(2x + 1).

Thus c(n + 1) = c(n) holds only at n = 0, whereas c(n + 1) = 2c(n) holds exactly for odd n.

**Lemma 2.** c(n) = 2^q − 1 only for n = 0, 1 (c = 1) and n = 3 (c = 3). Consequently, for n ≥ 4, c(n) < 2^p − 1 if and only if c(n) < 2^p.

*Proof.* For even n ≥ 2, c(n) = 2c(n − 1) is even. For n = 2x + 1, c(n) = C(2x + 2, x + 1)/2, and Legendre's formula gives v₂(C(2y, y)) = s₂(y), the number of ones in the binary expansion of y [3]. Indeed, v₂(t!) = Σ_{j≥1} ⌊t/2^j⌋ = t − s₂(t), and s₂(2y) = s₂(y). So c(n) is odd exactly when x + 1 is a power of two, that is, n = 2^M − 1. For M ≥ 3 write

C(2^M − 1, 2^(M−1) − 1) = ∏_{i=1}^{K} (2^M − i)/i,  K = 2^(M−1) − 1.

With i = 2^v u, u odd, the factor is (2^(M−v) − u)/u, a ratio of odd integers congruent to −1 modulo 2^(M−v). Since i < 2^(M−1), v ≤ M − 2. Factors with v ≤ M − 3 are ≡ −1 (mod 8). The single factor with v = M − 2 is i = 2^(M−2), equal to 3. As K is odd, the product is ≡ (−1)^(K−1) × 3 = 3 (mod 8), whereas 2^q − 1 ≡ 7 (mod 8) for q ≥ 3. Since c(7) = 35, the case M ≥ 3 would need q ≥ 6. The remaining cases M ≤ 2 are n = 0, 1, 3.

**Lemma 3 (parity).** For every n ≥ 1, 2^n/c(n) = w(⌈n/2⌉). Further w(m + 1)/w(m) = 2(m + 1)/(2m + 1) > 1, so w is strictly increasing.

*Proof.* For n = 2m this is the definition. For n = 2m − 1, C(2m, m) = 2C(2m − 1, m − 1) by Lemma 1, so 2^(2m−1)/C(2m − 1, m − 1) = 4^m/C(2m, m). The ratio follows from C(2m + 2, m + 1) = C(2m, m)(2m + 1)(2m + 2)/(m + 1)².

Thus 2^n/c(n) grows only from an even row to the next odd row and is unchanged from an odd row to the next even row.

**Lemma W.** For every m ≥ 1,

π(m + 1/4 − 1/(36m + 3)) < w(m)² < π(m + 1/4 + 0.07/m).

*Proof.* Robbins' form of Stirling's formula [2] states n! = √(2πn)(n/e)^n e^(r_n) with 1/(12n + 1) < r_n < 1/(12n). Applied to (2m)! and m!, it gives w(m)² = πm e^s with s = 2(2r_m − r_(2m)), and

ms > (36m − 1)/(12(12m + 1)) = 1/4 − 1/(36m + 3),  ms < (18m + 1)/(72m + 3) = 1/4 + 1/(288m + 12).

Now e^s > 1 + s, and for 0 < s < 1, e^s < 1 + s + s², since the tail of the exponential series is at most s²(e − 2). Here s < 19/(75m), so ms² < 0.0642/m, and 1/(288m + 12) + 0.0642/m < 0.07/m.

By rows, with θ the error term: for even n, (2^n/c(n))² = (π/2)(n + 1/2 + θ) with −2/(18n + 3) < θ < 0.28/n. For odd n, (2^n/c(n))² = (π/2)(n + 3/2 + θ) with −2/(18n + 21) < θ < 0.28/(n + 1). The two parities differ by about 0.72/n in log₂ c(n), which is small. It decides which row is the threshold row (Theorem C).

## 4. Proofs

*Theorem A.* For every n, c(n + 2)/c(n) equals 2(2x + 1)/(x + 1) = 4 − 2/(x + 1) when n = 2x and 2(2x + 3)/(x + 2) = 4 − 2/(x + 2) when n = 2x + 1, so c(n + 2) < 4c(n). The base cases are C(9, 4) = 126 < 127 = M_7 and C(10, 5) = 252 < 255 = M_8. If c(p + 2) ≤ M_p − 1, then c(p + 4) < 4(2^p − 2) = 2^(p+2) − 8 < M_(p+2). The odd chain starts at p = 7 and the even chain at p = 8. Theorem A also follows from Theorem B1, since p_2 = 7.

*Theorem B1.* Let p ≥ 7 and k ≥ 2, so p + k ≥ 9. Then

N(p) − p ≥ k ⟺ c(p + k) < 2^p − 1 (Lemma 1) ⟺ c(p + k) < 2^p (Lemma 2) ⟺ w(⌈(p + k)/2⌉) > 2^k (Lemma 3) ⟺ ⌈(p + k)/2⌉ ≥ m_k ⟺ p ≥ 2m_k − k − 1.

By Lemma W, w is unbounded, so m_k exists. The ratio w(m + 1)/w(m) is less than 2. Since w(m_k − 1) ≤ 2^k, this gives w(m_k) < 2^(k+1), hence m_(k+1) ≥ m_k + 1 and p_(k+1) > p_k.

*Theorem B2.* From w(m_k)² > 4^k and the upper bound of Lemma W, 4^k/π < m_k + 1/4 + 0.07/m_k. From w(m_k − 1)² ≤ 4^k and the lower bound, m_k − 3/4 − 1/(36m_k − 33) < 4^k/π. Substitute into p_k = 2m_k − k − 1 and use m_k ≥ 5 for k ≥ 2. The resulting wider interval always contains ⌈4^k/π − 1/4⌉, and contains a second integer only if the fractional part of 4^k/π − 1/4 is below 0.07/m_k or above 1 − 1/(36(m_k − 1)). The values for k ≤ 12 were computed exactly (Section 5). Since p_13 > 2×4^13/π − 14.53 > 42 722 815, the closed form for N(p) holds up to 42 700 000.

*Theorem B3.* Let N(p) − p = k, so p_k ≤ p < p_(k+1). Lower bound: p < p_(k+1) < 2×4^(k+1)/π, so πp/2 < 4^(k+1) and h(p) < k + 1. Upper bound: p > 2×4^k/π − k − 1.53, so πp/2 > 4^k(1 − (π/2)(k + 1.53)/4^k), and taking logarithms gives e(k). On the plateau k = 2, p ≥ 7 gives the value 2 − h(7). Since e(k) decreases and e(3) < 0.0851 < 2 − h(7), 2 − h(7) is the overall maximum. Within a plateau h increases, so the extreme values sit at p = p_k and p = p_(k+1) − 1, and the latter tends to −1 by Theorem B2. For the integer form, h(p) lies in (k − e(k), k + 1) on the plateau, and h(p) ≥ k exactly when p ≥ 2×4^k/π.

For the window count, write T_k = 2×4^k/π. It contains ⌈T_k⌉ − p_k = k + 1 + ⌈1/2 − 2φ_k⌉ integers. The bounds in B2 give −1.514 < 1/2 − 2φ_k < 0.528 for k ≥ 2, so the last ceiling is −1, 0 or 1.

*Theorem B4.* Writing Theorem B2 for k and k + 1 gives p_(k+1) − 4p_k = 3k + 7/2 + 2φ_(k+1) − 8φ_k. Since m_2 = 5 and m_3 = 21, this lies above 3k + 3.5 − 0.03 − 8.06 > 3k − 5 and below 3k + 3.5 + 2.01 + 0.12 < 3k + 6. For k ≥ 2, 3k − 5 > 0, and (3k + 6)/p_k → 0 because p_k > 2×4^k/π − k − 1.53.

*Theorem C.* At p = p_k, N(p) = p + k and N(p − 1) = N − 2, so c(N − 1) ≥ 2^(p−1) − 1 and, by Lemma 2, c(N − 1) ≥ 2^(p−1). If N were even, c(N) = 2c(N − 1) ≥ 2^p > M_p, a contradiction. For N = 2x + 1, c(N) = c(2x)(2x + 1)/(x + 1) ≥ 2^(p−1)(2 − 1/(x + 1)) = 2^p(1 − 1/(N + 1)). Directly from Theorem B1, N = p_k + k = 2m_k − 1.

## 5. Computations

The accompanying [verifier](tests/verify_np.py) checks finite instances of the statements. From the repository root, Python 3.10 or later is sufficient:

```sh
python3 -B tests/verify_np.py --quick
python3 -B tests/verify_np.py
```

The default run checks every p from 7 to 20000. The quick run stops at p = 1000 and is a smoke test, not a substitute for the default run. Neither mode writes a file unless `--json PATH` is supplied.

| Check | Default run | Quick run |
|---|---|---|
| Central coefficients from recurrence and math.comb | n = 0..20012 | n = 0..1012 |
| N(p), Theorem A, error bounds and threshold characterization | p = 7..20000 | p = 7..1000 |
| Pascal addition-only oracle for N(p) | p = 7..128 | p = 7..128 |
| Lemma W | m = 1..10006 | m = 1..506 |
| Direct scan for m_k | k = 1..8 | k = 1..8 |
| Exact threshold boundary checks | k = 1..12 | k = 1..8 |
| Special residue c(2^M − 1) modulo 8 | M = 3..20 | M = 3..12 |
| Ratio bounds | k = 2..11 | k = 2..7 |
| Threshold-row bounds | k = 3..12 | k = 3..8 |

The comparisons use Python integers. Machin's identity π = 16 arctan(1/5) − 4 arctan(1/239) gives a rational enclosure, with truncation errors propagated through every term. The scale is 10^90, and the total interval width is checked to be below 10^−80. The enclosure must decide each π-dependent comparison. If it cannot, the program fails instead of guessing. Agreement with a known 50-digit prefix is only a diagnostic check, not the justification of the enclosure.

For every threshold candidate, the program checks both 2^k C(2m_k,m_k) < 4^(m_k) and failure of that strict inequality at m_k − 1. Above the scan range, the candidate is suggested by the ceiling expression and is accepted only after these exact checks. The global upper error bound is checked without logarithms as 7×4^(D(p)−2) ≤ p. Logarithms use Decimal only to display approximate extrema and do not decide whether a check passes.

In the default range, D(p) changes at 38, 159, 646, 2601 and 10422. Its error D(p) − h(p) is largest at p = 7, about 0.270574, and smallest at p = 10421, about −0.999351. The [recorded result](tests/np_verification.json) states the actual run scope and check count. A normal run returns exit code 0 only after all checks pass. Runtime depends on the machine, especially for the large exact binomial coefficients at k = 12.

These are finite computational checks. The recurrence, math.comb and the addition-only comparison use the same Python integer implementation, so they are not independent arithmetic backends. The general statements rely on the proofs, and the all-k ceiling formula remains open.

## 6. Open question

Whether p_k = 2⌈4^k/π − 1/4⌉ − k − 1 holds for every k is NOT PROVED. It would follow if the fractional part of 4^k/π − 1/4 never came within about 4^(−k) of an integer. I know of no result on π that settles this. Theorems B1 to B4 and C do not depend on it. Sharper bounds from further terms of the Stirling series would narrow the exceptional band but would not remove it.

## 7. Remarks

1. The same carry-free principle is used in the work of Islam et al. (2022) [4]. For a given row n, they choose the base b = 10^d with d the number of decimal digits of c(n), so that b > c(n), and read the row off the blocks of (b + 1)^n. The condition c(n) < b is the same one used here. Their paper fixes the row and enlarges the base. This note fixes the base M_p and asks for the largest row. Jiu and Vignat [5] study related digital binomial identities using b-ary binomial coefficients. Those are different objects from the ordinary coefficients used here, and no theorem from that paper is needed in these proofs. Its 2019 correction is linked with the reference.
2. The ingredients are Pascal's rule, Legendre's formula, Robbins' bounds and elementary inequalities. Lemma 2 includes the short modular argument for c(2^M − 1) ≡ 3 (mod 8). This is not a claim of priority.
3. The approximation N(p) ≈ p + ½ log₂(πp/2) cannot be sharpened to p + ½ log₂(πp/2) + constant + o(1): N(p) − p is an integer, and N(p) − p − h(p) sweeps from about 0 down to almost −1 on each plateau.
4. The earlier note [1] states that from p = 38 on, row p + 3 is clean as well. Theorem B1 extends this statement to every k.

## References

1. J. Augustus, [Powers of two as carry-free Pascal rows in Mersenne bases](note.md), the preceding note in this repository.
2. H. Robbins, A remark on Stirling's formula, Amer. Math. Monthly 62 (1955), no. 1, 26-29. https://doi.org/10.2307/2308012
3. K. Conrad, [Proofs of integrality of binomial coefficients](https://kconrad.math.uconn.edu/blurbs/proofs/binomcoeffintegral.pdf), Section 5, for Legendre's factorial valuation formula.
4. M. S. Islam, M. R. Islam, M. S. Hossan, M. H. Kibria, Generating binomial coefficients in a row of Pascal's triangle from extensions of powers of eleven, Heliyon 8 (2022), no. 11, e11651. https://doi.org/10.1016/j.heliyon.2022.e11651, preprint https://arxiv.org/abs/2005.14490
5. L. Jiu, C. Vignat, On binomial identities in arbitrary bases, J. Integer Sequences 19 (2016), Article 16.5.5. [Paper](https://cs.uwaterloo.ca/journals/JIS/VOL19/Jiu/jiu3.pdf), [2019 correction](https://cs.uwaterloo.ca/journals/JIS/VOL19/Jiu/jiu3-corrigendum.pdf).
6. [OEIS A001405](https://oeis.org/A001405), the central coefficients C(n,⌊n/2⌋), as a sequence reference.

Text CC BY 4.0, code MIT.
