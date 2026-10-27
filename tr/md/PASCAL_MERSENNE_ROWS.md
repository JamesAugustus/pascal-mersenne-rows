# Mersenne tabanlarında ikinin kuvvetleri, eldesiz Pascal satırları

James Augustus

## Özet

$M_p$ = 2<sup>p</sup> − 1 olsun. $2^{p(p+2)}$ sayısı $M_p$ tabanında yazılınca haneleri tam olarak Pascal üçgeninin p + 2'nci satırındaki sayılar olur; her p ≥ 7 tamsayısı için hiçbir hane tabana ulaşmaz. Tek p için ortadaki hane, (p + 2) ile bir Katalan sayısının çarpımıdır. Asal çarpanları, hanenin kendisini hesaplamadan Legendre formülünden çıkıyor. Ekteki tarihsel tablolar, 14 Ekim 2026 çalışma listesindeki 52 Mersenne asal üssünü kapsıyor. Kullandığım araçlar klasiktir; bu not belirli bir taban ve satır seçimini kayda geçiriyor.

## 1. Kurulum

Her b tabanı için $(b+1)^n=\sum_{k=0}^{n}\binom{n}{k}b^{n-k}$. Katsayılar (b + 1)<sup>n</sup> sayısının b tabanındaki haneleri ancak her C(n,k) b'den küçükse oluyor, yani ortadaki katsayı b'den küçükse. 10 tabanında bu 11<sup>n</sup> için n ≤ 4'te tutuyor, n = 5'ten itibaren tutmuyor.

b = $M_p$ alıyorum; böylece b + 1 = 2<sup>p</sup> ve n = p + 2 oluyor. Üs buradan geliyor, (b + 1)<sup>n</sup> = `(2^p)^(p+2)` = $2^{p(p+2)}$. Burada p ≥ 2 bir tamsayıdır. Eldesiz yazım sonucu her p ≥ 7 tamsayısı için geçerlidir. Teorem 3 ve Sonuç 4'teki tek p durumu için n = 2x + 1 ve x = (p + 1)/2 alıyorum; iki orta katsayı C(n, x) = C(n, x + 1) olur.

[Şekil 1: satırın koordinatları (PDF)](../pdf/figures/coordinates.pdf)

## 2. Sonuçlar

**Teorem 1.** $\sum_{k=0}^{n}\binom{n}{k}M_p^{n-k}=2^{p(p+2)}$.

**Teorem 2.** Her p ≥ 7 tamsayısı için C(p + 2, ⌊(p + 2)/2⌋) < $M_p$. Bu yüzden p + 2'nci satırın her sayısı $M_p$ tabanında bir hanedir ve $2^{p(p+2)}$ $M_p$ tabanında o satır olarak yazılıyor.

**Teorem 3.** Tek p ≥ 7 için x = (p + 1)/2 olsun. C(2x + 1, x) = (2x + 1) $\mathrm{Cat}_x$, burada $\mathrm{Cat}_x=\frac{1}{x+1}\binom{2x}{x}$. Özellikle ortadaki hane (p + 2) $\mathrm{Cat}_{(p+1)/2}$ olur ve ikinci hane olan p + 2 onu böler.

**Sonuç 4.** Tek p ≥ 7 için (p + 3)/2 < q ≤ p + 2 olan her q asalı ortadaki haneyi tam bir kez böler. (p + 3)/2 asalsa ortadaki haneyi bölmez.

Örnek: p = 7. Taban 127, 2<sup>63</sup> = 128<sup>9</sup> sayısının haneleri 1, 9, 36, 84, 126, 126, 84, 36, 9, 1; 126 = 9 · 14 = 9 · $\mathrm{Cat}_4$. (p + 3)/2 = 5 asalı 126'yı bölmüyor.

## 3. Kanıtlar

*Teorem 1*, b = $M_p$ için binom teoremi.

*Teorem 2.* p'yi ikişer artırarak tek ve çift p üzerinde ayrı ayrı tümevarım yapıyorum. Tek p için başlangıç n = p + 2 = 9: C(9, 4) = 126 < 127 = M<sub>7</sub>. Adım için

$\frac{\binom{2x+3}{x+1}}{\binom{2x+1}{x}}=\frac{(2x+3)(2x+2)}{(x+1)(x+2)}=\frac{2(2x+3)}{x+2}<4$.

C(2x + 1, x) < $M_p$ ise C(2x + 3, x + 1) < 4 $M_p$ < 4 $M_p$ + 3 = $M_{p+2}$. Çift p için başlangıç p = 8: C(10, 5) = 252 < 255 = M<sub>8</sub>. n = 2x yazınca sonraki orta katsayı için

$\frac{\binom{2x+2}{x+1}}{\binom{2x}{x}}=\frac{2(2x+1)}{x+1}<4$.

Böylece $M_{p+2}$ = 4 $M_p$ + 3 ile aynı karşılaştırma çift p adımını da kanıtlar. İki tümevarım bütün p ≥ 7 tamsayılarını kapsar. p = 2, 3, 4, 5, 6 için orta katsayılar sırasıyla 6, 10, 20, 35, 70 olup 3, 7, 15, 31, 63 tabanlarını aşar.

*Teorem 3.* $\binom{2x+1}{x}=\frac{(2x+1)!}{x!(x+1)!}=(2x+1)\frac{(2x)!}{x!(x+1)!}=\frac{2x+1}{x+1}\binom{2x}{x}$.

*Sonuç 4.* Legendre formülüne göre q'nun C(n, x) içindeki üssü $v_q(n!)-v_q(x!)-v_q((x+1)!)$. x + 1 < q ≤ n ise n < 2q, yani v<sub>q</sub>(n!) = 1 ve öteki iki terim sıfır. q = x + 1 ise v<sub>q</sub>((x + 1)!) = 1 ve üs 0.

## 4. Hesaplar

Tablolar, 14 Ekim 2026 çalışma listesindeki 52 Mersenne asal üssü için merkez katsayı hesaplarını kaydediyor: p = 2, …, 136279841. Hesaplar gmpy2 ile yapıldı; ayrı bir kontrol betiği merkez katsayıları doğrudan gmpy2.comb ile yeniden hesapladı. Arşivdeki çıktısı 52 satır ve sıfır uyuşmazlık bildiriyor. İki hesap da GMP altyapısını kullandığı için bu, bağımsız bir aritmetik uygulamasıyla doğrulama değildir. Tarihsel kontrol merkez katsayıları ve tablo alanlarını kapsar; aşağıdaki komut satırı programlarıyla her Pascal satırını gezmek veya tam değerini kurmak değildir. Seçilmiş satırlar:

| p | ortadaki hanenin bit sayısı | $M_p$'nin bit sayısı | ortadaki hanenin onluk basamak sayısı |
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

h(p) = $\frac12\log_2(\pi p/2)$ için logaritmik fark asimptotik olarak h(p) − 2 olur. Tamsayı bit uzunlukları ayrıca yuvarlamaya bağlıdır. 7 ≤ p ≤ 37 için p + 2'nci satır $M_p$ tabanındaki son temiz satır. p = 38'den itibaren p + 3'üncü satır da temiz.

## 5. Notlar

1. Asallığın bir rolü yok. Eldesiz satır sonucu her p ≥ 7 tamsayısı için geçerlidir; Teorem 3 ve Sonuç 4'te tek p koşulu korunur. Örneğin M<sub>11</sub> = 23 · 89 da temiz bir satır veriyor. Mersenne asal üslerini yalnızca deneme olarak kullandım.
2. Kullandığım parçalar standarttır: binom teoremi, Legendre formülü, Teorem 3'teki eşitlik ve 11'in kuvvetleri deseninin keyfi tabanlara genişletilmesi [2, 3]. b = $M_p$, n = p + 2 seçimini literatürde bulamadım, ama aramam kısaydı.
3. Haneler birbirinden üretilebiliyor, $R_{k+1}=R_k\frac{n-k}{k+1}$, ve değer Horner kuralıyla geri kuruluyor. Bu yineleme, büyüyen bir katsayıyı en çok n olan bir tamsayıyla çarpar ve tam bölme yapar; maliyetsiz değildir. Horner ile tam değeri kurmak ayrıca büyük tamsayı çarpmaları gerektirir.
4. Ortadaki hane Katalan sayısı kullanmadan, yalnız toplamayla da bulunuyor. Her satırın ortası, bir önceki satırın ortası ile komşusunun toplamı, C(9, 4) = C(8, 4) + C(8, 3) = 70 + 56. İlk formülümde Katalan sayısı vardı, sonra onu bu toplamalı biçime çevirdim.

## 6. Kod

`mersenne_rows.py` ve `mersenne_rows_gmp.c` (GMP'li C), satır katsayılarını üretir ve her katsayının tabandan küçük olup olmadığını `clean` ile bildirir. Satır yalnız p ≤ 20 için ekrana yazılır. Değer, üç aday asal modülden tabanla aralarında asal olanlarda $2^{p(p+2)}$ ile karşılaştırılır; `moduli=m/3` kullanılan modül sayısıdır. Tabanla ortak çarpanı olan modüller, boş bir doğrulama vermemek için atlanır. Kullanılabilir modül kalmazsa `value(mod)=unavailable`, `clean=unchecked` ve 1 çıkış kodu verilir; satır ve tam değer hesaplanmaz. `full` seçeneği ayrıca tam tamsayı eşitliğini karşılaştırır.

Değer kontrolleri, binom eşitliğinin uygulamadaki tutarlılığını sınar; bağımsız bir matematiksel kanıt veya asallık testi değildir. Gösterim açısından belirleyici koşul, en büyük katsayının tabandan küçük olmasıdır. Her iki program da n + 1 katsayıyı gezer; ekrana satır basılmaması bu işi ortadan kaldırmaz. `full` çıktısının bit uzunluğu p(p + 2) + 1'dir. Çok büyük üslerde bu satır taraması ve tam değer belleği pratik olmayabilir; merkez katsayısını doğrudan hesaplamak farklı bir iştir.

```
cc -O2 -o mersenne_rows_gmp mersenne_rows_gmp.c -lgmp
./mersenne_rows_gmp 7 full
./mersenne_rows_gmp 132049
```

`tr/tables/` klasöründe 52 üslük çalışmaya ait dört Türkçe tablo var. Teoremler ve kanıtları, ortadaki haneler, listedeki ilk 50 üssün ortadaki haneleri ve bunların çarpanları. p = 7, …, 61 için GMP'siz bir kontrol, yanındaki `ctcpu-hunter` deposunda `journal_tests.c` içindeki T21<sub>m</sub>ersenne<sub>r</sub>ow testi.

## Kaynaklar

1. Binom teoremi. https://mathworld.wolfram.com/BinomialTheorem.html
2. L. Jiu, C. Vignat, On binomial identities in arbitrary bases, J. Integer Sequences 19 (2016). https://arxiv.org/abs/1602.04149
3. M. S. Islam ve arkadaşları, Generating binomial coefficients in a row of Pascal's triangle from extensions of powers of eleven, Heliyon (2022). https://arxiv.org/abs/2005.14490
4. Legendre formülü. https://en.wikipedia.org/wiki/Legendre%27s<sub>f</sub>ormula
5. OEIS A001405 (orta binom katsayıları), A000108 (Katalan sayıları). https://oeis.org
6. GIMPS, bilinen Mersenne asalları listesi. https://www.mersenne.org/primes/

Metin CC BY 4.0, kod MIT.
