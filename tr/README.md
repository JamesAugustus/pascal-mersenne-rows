# Mersenne tabanlarında Pascal satırları

Bu çalışma, sayıları Pascal yapılarıyla göstermek için araştırdığım
yöntemlerden biri. Burada ikinin belirli kuvvetlerini Mersenne tabanlarında
Pascal satırlarıyla yazıyorum. Kanıtı matematik notunda; örneğini yeniden
hesaplamak için Python ve C programları da üst klasörde.
[English](../README.md)

## Sonuç ve örnek

Matematik notu, seçtiğim taban ve satır ilişkisinde hanelerin hangi
koşullarda elde taşımadan yazılabildiğini gösteriyor: her p ≥ 7 tamsayısı
için p + 2 satırı, 2^p − 1 tabanında eldesizdir.

Örneğin 127 tabanında şu haneler ikinin 63. kuvvetini gösterir:

```text
1 9 36 84 126 126 84 36 9 1
```

Bu tabanda 126 tek bir hanedir. Bütün haneler 127'den küçük olduğu için
elde taşıma gerekmez. Bu sonuç, genel bir asallık testi değildir.

## Nasıl yaptım?

Binom teoremindeki Pascal katsayılarını seçtiğim tabanın haneleri
olarak kullandım. Programlar katsayıları hesaplıyor, tabana sığıp sığmadıklarını
ve bu hanelerin beklenen ikinin kuvvetini verdiğini kontrol ediyor.
Böylece eldesiz satırı yeniden üretebilir, katsayıların ne zaman gerçek
hane olabildiğini inceleyebilirsin. Değer karşılaştırması, zaten binom
teoreminden gelen eşitliğin kodda doğru hesaplandığını sınar; ayrı bir
matematiksel kanıt veya asallık testi değildir.

Formüller, kanıtlar ve kaynakça [matematik notunda](note.pdf)
([metin biçimi](note.md)); hanelerin konumları [şekilde](coordinates_tr.pdf).

## Nasıl çalıştırılır?

Python 3 yeterli; ek paket kurulumu gerekmez. Ana proje klasöründe:

```sh
python3 mersenne_rows.py 7 full
```

Windows'ta `py -3 mersenne_rows.py 7 full` kullanılır. Sonuçta `clean=yes`,
`value(mod)=ok` ve `value(full)=ok` görülür. `clean=yes`, bütün katsayıların
tabandan küçük olduğunu, yani elde taşıma gerekmediğini belirtir. `64 bits`, bu örnekteki sonucun
uzunluğudur; sabit bir 64 bit sınırı değildir. `moduli=3/3`, üç aday
modülün üçünün de kullanıldığını belirtir; tabanla ortak çarpanı olanlar
atlanır. Hiçbiri uygun değilse program kontrol yapılamadığını bildirir.

Her iki program da n = p + 2 satırının n + 1 katsayısını gezer. `full`
sonucu p(p + 2) + 1 bit tutar; büyük üslerde zaman ve bellek bedeli hızla
büyür. Bu komutlar, 52 üslük tarihsel tabloların büyük merkez katsayılarını
hesaplamak için kullanılan ayrı programların yerine geçmez.

## Kurulum ve test

Kurulum isteğe bağlıdır. Paketi kendi kullanıcı klasörüne kopyalamak için:

```sh
python3 setup/install.py "$HOME/Mersenne"
```

Windows: `setup\install.bat "%USERPROFILE%\Mersenne"`.
macOS: `./setup/install.command "$HOME/Mersenne"`.
Kurulum betiği Python veya GMP indirmez; hedefte farklı içerikli bir dosya
varsa üzerine yazmadan durur. Test: `python3 -B tests/test_local.py`.

İsteğe bağlı C sürümü için C derleyicisi ve GMP gerekir:

```sh
cc -O2 -o mersenne_rows_gmp mersenne_rows_gmp.c -lgmp
./mersenne_rows_gmp 7 full
```

## Dosyalar ve kullanım koşulları

- Üst klasördeki `setup/`: kurulum; `tests/`: program ve kurulum testleri.
- Üst klasördeki `tables/`: İngilizce tablolar; buradaki `tables/`: Türkçe tablolar.
- `coordinates_tr.pdf`: Türkçe şekil.
- `note.md`, `note.pdf`: matematik notunun metin ve PDF biçimleri.
- Lisanslar: tüm kaynak kodları, başlatıcılar, kurulum dosyaları ve testler
  [MIT](../LICENSE) kapsamındadır. İngilizce ve Türkçe belgeler, PDF’ler,
  şekiller, tablolar ve atıf bilgileri [CC BY 4.0](../LICENSE-CC-BY-4.0)
  kapsamındadır. Telif hakkı © 2026 James Augustus. Her lisans belirtilen
  dosya grubuna uygulanır; bütün dosyalar için iki lisans arasında seçim sunulmaz.
- [CITATION.cff](../CITATION.cff): çalışmaya kaynak gösterme bilgileri.

James Augustus · jamesaugustus1313@gmail.com
