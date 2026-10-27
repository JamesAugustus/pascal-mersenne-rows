#!/usr/bin/env python3
"""Finite exact checks for NP_CARRY_FREE_ROW_BOUND.md. No claim of proof by testing.

Default: all p=7..20000, threshold k=1..12, special parity rows M=3..20.
--quick: p=7..1000, k=1..8, M=3..12. Python standard library only.
"""
import argparse
from decimal import Decimal, localcontext
from math import comb
from pathlib import Path
import json
import time


def pi_interval(digits=90):
    """Integer enclosure from Machin's identity, including truncation error.

For each atan(1/x), floor truncation of the power and division contributes
less than two scaled units per term. The remaining alternating tail is
less than one unit when the power becomes zero. Weighted errors are added.
"""
    scale = 10 ** digits
    def atan_inverse(x):
        total, power, denominator, sign, count = 0, scale // x, 1, 1, 0
        while power:
            total += sign * (power // denominator)
            power //= x*x
            denominator += 2
            sign = -sign
            count += 1
        return total, 2*count+1
    a, ea = atan_inverse(5)
    b, eb = atan_inverse(239)
    value, error = 16*a-4*b, 16*ea+4*eb
    return value-error, value+error, scale


def pi_times_less(x, y, interval):
    """Decide pi*x < y using the whole enclosure, never its midpoint."""
    lo, hi, scale = interval
    if hi*x < y*scale:
        return True
    if lo*x > y*scale:
        return False
    raise ArithmeticError('pi enclosure cannot decide this comparison')


def central_coefficients(limit):
    values = [1]
    for n in range(limit):
        if n % 2:
            values.append(2*values[-1])
        else:
            x = n//2
            q, remainder = divmod(values[-1]*(2*x+1), x+1)
            if remainder:
                raise ArithmeticError('nonintegral central recurrence')
            values.append(q)
    return values


def threshold_candidate(k, interval):
    """ceil(4^k/pi - 1/4), a candidate which must still be verified."""
    _, hi, scale = interval
    m = max(1, (4**(k+1)*scale//hi-1)//4-2)
    while pi_times_less(4*m+1, 4**(k+1), interval):
        m += 1
    return m


def verify(quick=False):
    started = time.monotonic()
    pmax, kmax, special_max = (1000, 8, 12) if quick else (20000, 12, 20)
    nmax, kscan = pmax+12, min(8, kmax)
    checks = 0
    def check(condition, message):
        nonlocal checks
        checks += 1
        if not condition:
            raise AssertionError(message)
    pi = pi_interval()
    lo, hi, scale = pi
    # A diagnostic agreement with known digits, not the proof of enclosure.
    known = 314159265358979323846264338327950288419716939937510
    check(lo//10**40 == hi//10**40 == known, 'known 50-digit pi prefix')
    check((hi-lo)*10**80 < scale, 'pi interval width below 10^-80')

    c = central_coefficients(nmax)
    check(c[0] == c[1] == 1, 'c(0)=c(1)=1')
    for n in range(nmax+1):
        check(c[n] == comb(n,n//2), f'central coefficient {n}')
    for n in range(nmax):
        check((c[n+1] == c[n]) == (n == 0), f'equality {n}')
        check(c[n+1] <= 2*c[n], f'doubling bound {n}')
        check((c[n+1] == 2*c[n]) == bool(n%2), f'doubling parity {n}')
        if n:
            check(c[n+1] > c[n], f'strict growth {n}')
    check([n for n,x in enumerate(c) if x&(x+1)==0] == [0,1,3], 'Mersenne central values')
    for m in range(3,special_max+1):
        n = (1<<m)-1
        check(comb(n,n//2)%8 == 3, f'special residue M={m}')
    print(f'PASS central coefficients and parity: n=0..{nmax}, M=3..{special_max}',flush=True)

    # A genuinely different construction for small rows: Pascal additions.
    row = [1]
    small = []
    for n in range(150):
        small.append(max(row))
        check(max(row) == c[n], f'addition-only Pascal oracle n={n}')
        check(sum(row) == 1<<n, f'Pascal row sum n={n}')
        row = [1]+[a+b for a,b in zip(row,row[1:])]+[1]
    d, n = {}, 0
    for p in range(7,pmax+1):
        base = (1<<p)-1
        while c[n+1] < base:
            n += 1
        d[p] = n-p
        check(c[n] < base <= c[n+1], f'last clean row p={p}')
        check(c[p+2] < base, f'Theorem A p={p}')
        check(7*4**(d[p]-2) <= p, f'exact upper error constant p={p}')
        check(pi_times_less(p,2*4**(d[p]+1),pi), f'lower error bound p={p}')
        if p <= 128:
            independent = max(j for j,value in enumerate(small) if value < base)
            check(n == independent, f'addition-only N(p) p={p}')
    for p in range(7,pmax):
        check(d[p+1]-d[p] in (0,1), f'plateau step p={p}')
    for p in range(2,7):
        check(c[p+2] >= (1<<p)-1, f'small-p exception p={p}')
    transitions = [p for p in range(8,pmax+1) if d[p] > d[p-1]]
    expected = [p for p in (38,159,646,2601,10422) if p <= pmax]
    check(transitions == expected, 'transition table')
    print(f'PASS direct N(p): p=7..{pmax}, transitions={transitions}',flush=True)

    for m in range(1,nmax//2+1):
        square, power = c[2*m]**2, 1<<(4*m)
        check(pi_times_less(square*(144*m*m+48*m-1),4*(36*m+3)*power,pi), f'Lemma W lower m={m}')
        check(not pi_times_less(square*(400*m*m+100*m+28),400*m*power,pi), f'Lemma W upper m={m}')
    mk, centers = {}, {}
    m, cm, k = 0, 1, 1
    while k <= kscan:
        m += 1
        cm = cm*2*(2*m-1)//m
        while k <= kscan and (cm<<k) < 1<<(2*m):
            mk[k], centers[k] = m, cm
            k += 1
    for k in range(1,kmax+1):
        candidate = threshold_candidate(k,pi)
        if k in mk:
            check(mk[k] == candidate, f'scanned threshold k={k}')
        else:
            cm = comb(2*candidate,candidate)
            mk[k],centers[k] = candidate,cm
        m, cm = mk[k],centers[k]
        previous, remainder = divmod(cm*m,2*(2*m-1))
        check(remainder == 0, f'previous central coefficient k={k}')
        check(cm<<k < 1<<(2*m), f'threshold passes k={k}')
        check(previous<<k >= 1<<(2*m-2), f'previous threshold fails k={k}')
        print(f'PASS threshold k={k}: m={m}, p={2*m-k-1}',flush=True)
    pk = {k:2*m-k-1 for k,m in mk.items()}
    for k in range(2,kmax+1):
        m,p = mk[k],pk[k]
        # Both detailed B2 bounds by integer cross-multiplication.
        check(not pi_times_less(400*m*m+100*m+28,400*m*4**k,pi), f'B2 lower k={k}')
        check(pi_times_less(144*m*m-252*m+104,144*(m-1)*4**k,pi), f'B2 upper k={k}')
        check(pi_times_less(p,2*4**k,pi), f'coarse threshold upper k={k}')
        check(not pi_times_less(100*p+100*k+153,200*4**k,pi), f'coarse threshold lower k={k}')
        if k < kmax:
            delta=pk[k+1]-4*p
            check(3*k-5 < delta < 3*k+6, f'threshold ratio k={k}')
        if k >= 3:
            n=p+k
            middle=centers[k]//2
            check(n==2*m-1 and n%2==1, f'threshold row parity k={k}')
            check(middle < (1<<p)-1 <= centers[k], f'threshold last clean row k={k}')
            check(middle*(n+1) >= n<<p, f'Theorem C lower k={k}')
    # The k=13 lower bound certifies the finite closed-form range.
    check(pi_times_less(100*42700000+100*13+153,200*4**13,pi), 'next threshold beyond 42700000')
    windows=[]
    for p in range(7,pmax+1):
        value=max(k for k in pk if pk[k] <= p)
        check(d[p] == value, f'threshold characterization p={p}')
        floor_h=0
        while not pi_times_less(p,2*4**(floor_h+1),pi):
            floor_h+=1
        inside=pi_times_less(p,2*4**d[p],pi)
        check(d[p] == floor_h+int(inside), f'floor formula p={p}')
        if inside: windows.append(p)
    with localcontext() as ctx:
        ctx.prec=60
        approx_pi=Decimal(lo+hi)/(2*scale)
        errors={p:Decimal(v)-(approx_pi*p/2).ln()/(2*Decimal(2).ln()) for p,v in d.items()}
        p_min=min(errors,key=errors.get);p_max=max(errors,key=errors.get)
        extrema={'minimum':{'p':p_min,'value':str(errors[p_min])},'maximum':{'p':p_max,'value':str(errors[p_max])}}
    result={'mode':'quick' if quick else 'full','status':'PASS','checks':checks,
            'scope':{'p_min':7,'p_max':pmax,'central_n_max':nmax,'threshold_k_max':kmax,'scanned_k_max':kscan,
                     'special_parity_M_max':special_max,'addition_oracle_p_max':128},
            'pi_interval':{'lower_numerator':str(lo),'upper_numerator':str(hi),'denominator':str(scale)},
            'thresholds':[{'k':k,'m':mk[k],'p':pk[k]} for k in sorted(pk)],
            'transitions':transitions,'floor_correction_windows':windows,'display_only_decimal_extrema':extrema,
            'elapsed_seconds':round(time.monotonic()-started,3)}
    print(f'PASS {checks} checks, mode={result["mode"]}. Finite checks do not replace the proofs.',flush=True)
    return result


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--quick',action='store_true')
    parser.add_argument('--json',type=Path,help='optional result file, no output file by default')
    args=parser.parse_args(argv)
    result=verify(args.quick)
    if args.json:
        args.json.write_text(json.dumps(result,indent=2)+'\n')
    return 0

if __name__=='__main__':
    raise SystemExit(main())
