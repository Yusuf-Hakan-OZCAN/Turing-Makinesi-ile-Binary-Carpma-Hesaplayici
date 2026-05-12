# Turing Makinesi ile Binary Çarpma Hesaplayıcı

Özdevinirler Kuramı (Otomata Teorisi) dersi Final Ödevi 1 kapsamında geliştirilmiştir.

İki ikili (binary) sayının çarpımını **tek bantlı bir Turing Makinesi** simülatörü ile hesaplar. Çarpma işlemi, bilgisayar mimarisinde de kullanılan **kaydır ve topla (shift & add)** yöntemiyle gerçekleştirilir. Makine her adımı (durum, okunan sembol, yazılan sembol, hareket yönü ve bant içeriği) ekrana yazdırarak çalışır.

## Bant Formatı

Makine bandı şu şekilde başlatılır:

```
A * B =
```

- `*` → iki operandı ayıran sembol
- `=` → sonuç alanının başlangıcı

Sonuç, `=` işaretinin sağına yazılır.

## Turing Makinesi Tanımı

Makine **M = (Q, Σ, Γ, δ, q₀, B, F)** yedilisiyle tanımlanır:

| Bileşen | Değer |
|---|---|
| Q | `{ q_start, q_find_b, q_scan, q_bit0, q_bit1, q_add, q_shift, q_accept }` |
| Σ | `{ 0, 1, *, = }` |
| Γ | `{ 0, 1, *, =, x, y, _ }` |
| q₀ | `q_start` |
| B | `_` (boş hücre) |
| F | `{ q_accept }` |

İşlenmiş bitler bant üzerinde işaretlenir: `0 → x`, `1 → y`. Böylece her bit yalnızca bir kez kullanılır.

## Durumlar

- **q_start** — A operandını okur, `*` görene kadar sağa hareket eder.
- **q_find_b** — B operandının sağ ucundaki `=` işaretine kadar gider.
- **q_scan** — B üzerinde sağdan sola tarayıp henüz işlenmemiş ilk biti bulur.
- **q_bit1 / q_bit0** — Aktif biti `y`/`x` olarak işaretler.
- **q_add** — Kaydırılmış A'yı mevcut sonuca ikili toplama ile ekler.
- **q_shift** — Kaydırma sayacını artırır, taramayı yeniden başlatır.
- **q_accept** — Tüm bitler işlendiğinde kabul durumu.

## Diyagramlar

| Dosya | İçerik |
|---|---|
| [durum_diyagrami.png](durum_diyagrami.png) | Durum geçiş diyagramı |
| [gecis_tablosu.png](gecis_tablosu.png) | δ geçiş fonksiyonu tablosu |
| [örnekler.png](örnekler.png) | Çalıştırma örnekleri |

## Kurulum ve Çalıştırma

Python 3.7+ yeterlidir, ek bağımlılık yoktur.

```bash
python tm_carpma.py
```

Program iki binary sayı isteyecek, ardından adım adım simülasyonu ve sonucu yazdıracaktır.

Programatik kullanım için:

```python
from tm_carpma import carp
sonuc = carp("11", "10", log=False)   # "110"  (3 × 2 = 6)
```

## Örnek Çıktı

`11 × 10` (yani 3 × 2) için:

```
>>> Başlangıç bandı: [1]1*10=
Adım 1 | q_start  | Okundu: 1 | Yazıldı: 1 | Hareket: R
Adım 2 | q_start  | Okundu: 1 | Yazıldı: 1 | Hareket: R
Adım 3 | q_start  | Okundu: * | Yazıldı: * | Hareket: R
Adım 4 | q_find_b | Okundu: 1 | Yazıldı: 1 | Hareket: R
Adım 5 | q_find_b | Okundu: 0 | Yazıldı: 0 | Hareket: R
Adım 6 | q_find_b | Okundu: = | Yazıldı: = | Hareket: L
Adım 7 | q_bit0   | Okundu: 0 | Yazıldı: x | Hareket: -
Adım 8 | q_bit1   | Okundu: 1 | Yazıldı: y | Hareket: -
          >> Sonuca eklenecek: 110
...
>>> KABUL. Final bant: 11*yx=110
```

## Test Sonuçları

| A (binary) | B (binary) | Sonuç | Decimal Doğrulama |
|---|---|---|---|
| 11 | 10 | 110 | 3 × 2 = 6 |
| 101 | 11 | 1111 | 5 × 3 = 15 |
| 1010 | 101 | 110010 | 10 × 5 = 50 |
| 111 | 111 | 110001 | 7 × 7 = 49 |
| 1100 | 1010 | 1111000 | 12 × 10 = 120 |
| 1 | 0 | 0 | 1 × 0 = 0 (kenar durum) |
| 1111 | 1 | 1111 | 15 × 1 = 15 |

Tüm test girdilerinde sonuçlar matematiksel olarak doğrulanmıştır (7/7).

## Dosyalar

```
tm_carpma.py          Turing Makinesi simülatörü (ana kod)
durum_diyagrami.png   Durum geçiş diyagramı
gecis_tablosu.png     δ geçiş fonksiyonu tablosu
örnekler.png          Çalıştırma örnekleri
```
