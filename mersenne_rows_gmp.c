/* Powers of two as carry-free Pascal rows in Mersenne bases.
   Author: James Augustus. October 2026. License: MIT.

   Base M_p = 2^p - 1, row n = p + 2. In base M_p, 2^p is written "11".
   Digits of the row, left to right: 1, n, n(n-1)/2, ... (binomial coefficients).
   Two checks:
     1) clean: every digit is below the base
     2) value: Horner's rule v = v*base + digit gives 2^(p(p+2))
   For large p the full value is huge, so by default the value is checked
   modulo the coprime members of three fixed primes; the used count is reported.
   Pass "full" as second argument for exact comparison.

   Build: cc -O2 -o mersenne_rows_gmp mersenne_rows_gmp.c -lgmp
   Run:   ./mersenne_rows_gmp 7 full
          ./mersenne_rows_gmp 132049
*/
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <limits.h>
#include <stdint.h>
#include <gmp.h>

#define NQ 3

static int usage(const char *program) {
    fprintf(stderr, "Usage: %s [p [full]] (decimal p: 2..ULONG_MAX-3)\n", program);
    return 2;
}

int main(int argc, char **argv) {
    unsigned long p = 7;
    int full;
    if (argc == 2 && strcmp(argv[1], "--help") == 0) {
        printf("Usage: %s [p [full]]\nDecimal p: 2..%lu (default 7). Full requires p*(p+2) to fit unsigned long and mp_bitcnt_t.\n",
               argv[0], ULONG_MAX - 3);
        return 0;
    }
    if (argc > 3) return usage(argv[0]);
    if (argc > 1) {
        const char *s = argv[1];
        char *end;
        const char *c;
        if (!*s) return usage(argv[0]);
        for (c = s; *c; c++) if (*c < '0' || *c > '9') return usage(argv[0]);
        errno = 0;
        p = strtoul(s, &end, 10);
        if (errno == ERANGE || *end || p < 2 || p > ULONG_MAX - 3) return usage(argv[0]);
    }
    if (argc == 3 && strcmp(argv[2], "full") != 0) return usage(argv[0]);
    full = argc == 3;
    unsigned long n = p + 2;                     /* row number */
    unsigned long k;
    int clean = 1, value_mod = 1, value_full = 1;
    int active[NQ], used = 0;
    mpz_t b, R, v, t, q[NQ], bq[NQ], h[NQ], e;

    /* n+1 is used by k+1 on the last iteration; p <= ULONG_MAX-3 keeps it safe.
       Check the exponent value before multiplication or narrowing to GMP's bit index. */
    if (full && (p > ULONG_MAX / n ||
                 (uintmax_t)p > (uintmax_t)((mp_bitcnt_t)-1) / (uintmax_t)n)) {
        fprintf(stderr, "full exponent p*(p+2) cannot fit unsigned long or mp_bitcnt_t\n");
        return 2;
    }

    mpz_inits(b, R, v, t, e, NULL);

    /* check moduli: 2^127 - 1, 2^89 - 1, 2^61 - 1 (all three prime) */
    {
        unsigned long us[NQ] = { 127, 89, 61 };
        int i;
        for (i = 0; i < NQ; i++) {
            mpz_inits(q[i], bq[i], h[i], NULL);
            mpz_ui_pow_ui(q[i], 2, us[i]);
            mpz_sub_ui(q[i], q[i], 1);
            /* gcd(base,q) = gcd((2^p mod q)-1,q), without allocating base. */
            mpz_set_ui(t, 2);
            mpz_powm_ui(bq[i], t, p, q[i]);
            mpz_sub_ui(bq[i], bq[i], 1);
            mpz_mod(bq[i], bq[i], q[i]);
            mpz_gcd(t, bq[i], q[i]);
            active[i] = mpz_cmp_ui(t, 1) == 0;
            used += active[i];
        }
    }

    if (used == 0) {
        printf("p=%lu row=%lu clean=unchecked value(mod)=unavailable moduli=0/%d\n", p, n, NQ);
        fprintf(stderr, "No coprime check modulus; row and full checks were not run.\n");
        for (int i = 0; i < NQ; i++) mpz_clears(q[i], bq[i], h[i], NULL);
        mpz_clears(b, R, v, t, e, NULL);
        return 1;
    }
    mpz_ui_pow_ui(b, 2, p);
    mpz_sub_ui(b, b, 1);                         /* base = M_p */
    mpz_set_ui(R, 1);                            /* leftmost digit 1 */
    mpz_set_ui(v, 0);
    for (k = 0; k <= n; k++) {
        int i;
        if (p <= 20) gmp_printf("%Zd ", R);
        if (mpz_cmp(R, b) >= 0) clean = 0;      /* digit reaches the base */
        for (i = 0; i < NQ; i++) {               /* h = h*base + digit (mod q) */
            if (!active[i]) continue;
            mpz_mul(h[i], h[i], bq[i]);
            mpz_add(h[i], h[i], R);
            mpz_mod(h[i], h[i], q[i]);
        }
        if (full) {                              /* v = v*base + digit = (v << p) - v + digit */
            mpz_mul_2exp(t, v, p);
            mpz_sub(v, t, v);
            mpz_add(v, v, R);
        }
        mpz_mul_ui(R, R, n - k);                 /* next digit */
        mpz_divexact_ui(R, R, k + 1);
    }
    if (p <= 20) printf("\n");

    mpz_set_ui(e, p);
    mpz_mul_ui(e, e, n);                         /* exponent p(p+2) */
    {
        int i;
        mpz_t two, expected;
        mpz_inits(two, expected, NULL);
        mpz_set_ui(two, 2);
        for (i = 0; i < NQ; i++) {
            if (!active[i]) continue;
            mpz_powm(expected, two, e, q[i]);
            if (mpz_cmp(h[i], expected) != 0) value_mod = 0;
        }
        mpz_clears(two, expected, NULL);
    }

    printf("p=%lu row=%lu clean=%s value(mod)=%s",
           p, n, clean ? "yes" : "NO", value_mod ? "ok" : "WRONG");
    if (full) {
        mpz_set_ui(t, 0);
        mpz_setbit(t, (mp_bitcnt_t)(p * n));     /* checked before narrowing */
        value_full = mpz_cmp(v, t) == 0;
        printf(" value(full)=%s (%zu bits)", value_full ? "ok" : "WRONG",
               mpz_sizeinbase(v, 2));
    }
    printf(" moduli=%d/%d\n", used, NQ);
    for (int i = 0; i < NQ; i++) mpz_clears(q[i], bq[i], h[i], NULL);
    mpz_clears(b, R, v, t, e, NULL);
    return (clean && value_mod && value_full) ? 0 : 1;
}
