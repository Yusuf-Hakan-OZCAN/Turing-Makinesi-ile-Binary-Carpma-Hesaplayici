"""
Final Ödev 1: Turing Makinesi ile Binary Çarpma Hesaplayıcı
-----------------------------------------------------------
Tek bantlı bir Turing Makinesi simülatörü ile iki ikili (binary)
sayının çarpımını "kaydır ve topla" (shift & add) yöntemiyle hesaplar.

Bant formatı:  A * B = <sonuc>
  - '*' karakteri: iki operandı ayırır
  - '=' karakteri: sonuç alanının başlangıcını belirtir
"""

BLANK = "_"   # Boş hücre sembolü


# ---------------------------------------------------------------
# 1) BANT (Tape) - Turing Makinesinin sonsuz şeridi
# ---------------------------------------------------------------
class Bant:
    """Turing Makinesinin bandı. Gerektikçe iki yöne de genişler."""

    def __init__(self, giris: str):
        self.hucreler = list(giris)
        self.kafa = 0

    def oku(self) -> str:
        if 0 <= self.kafa < len(self.hucreler):
            return self.hucreler[self.kafa]
        return BLANK

    def yaz(self, sembol: str):
        # Kafa banttan dışarı çıkmışsa banti genişlet
        while self.kafa >= len(self.hucreler):
            self.hucreler.append(BLANK)
        while self.kafa < 0:
            self.hucreler.insert(0, BLANK)
            self.kafa += 1
        self.hucreler[self.kafa] = sembol

    def sag(self):
        self.kafa += 1

    def sol(self):
        self.kafa -= 1

    def goster(self) -> str:
        """Bandı, kafa pozisyonu [köşeli parantez] içinde olacak şekilde döner."""
        parcalar = []
        for i, h in enumerate(self.hucreler):
            parcalar.append(f"[{h}]" if i == self.kafa else h)
        return "".join(parcalar)

    def icerik(self) -> str:
        return "".join(self.hucreler)


# ---------------------------------------------------------------
# 2) TURING MAKİNESİ - Durum, geçiş ve simülasyon
# ---------------------------------------------------------------
class TuringMakinesi:
    """
    Durumlar:
      q_start  : Başlangıç. * karakterini bulmak için sağa hareket eder.
      q_find_b : İkinci sayının (B) sağ ucunu (=) bulmak için sağa gider.
      q_scan   : B'nin en sağındaki işaretsiz biti bulmak için sola gider.
      q_bit1   : Aktif bit '1' → A'yı sonuca eklemek üzere "=" işaretine git.
      q_bit0   : Aktif bit '0' → ekleme yok, sadece kaydırma yapılacak.
      q_add    : Sonucu (kaydırılmış) A ile topla.
      q_shift  : A'yı bir bit sola kaydır (sonuna 0 ekle).
      q_accept : Tüm bitler tüketildi, sonuç hazır.
    """

    def __init__(self, a: str, b: str, log: bool = True):
        # Bandı kuralda istenen formata göre hazırla: A*B=
        self.A_orijinal = a
        self.B_orijinal = b
        self.bant = Bant(f"{a}*{b}=")
        self.durum = "q_start"
        self.log = log
        self.adim_sayisi = 0
        # Çarpma sürecinde A'nın kaydırılmış kopyasını burada tutarız;
        # bant üzerindeki "modelleme" mantığında bu, A'nın sonuna 0 ekleyerek
        # bandı güncellemekle eşdeğerdir.
        self.A_kayan = a
        # İşlenmiş bitleri işaretlemek için 'x' ve 'y' kullanırız:
        #   '0' -> 'x' (işlenmiş 0)
        #   '1' -> 'y' (işlenmiş 1)

    # ---- Yardımcı: Adım kaydı ----
    def _kaydet(self, okunan: str, yazilan: str, hareket: str):
        self.adim_sayisi += 1
        if self.log:
            print(
                f"Adım {self.adim_sayisi:>3} | Durum: {self.durum:<9} "
                f"| Okundu: {okunan} | Yazıldı: {yazilan} | Hareket: {hareket}"
            )
            print(f"          Bant: {self.bant.goster()}")

    # ---- Yardımcı: Bant üzerindeki B'nin sağdan ilk işaretsiz bitini bul ----
    def _sonraki_bit(self):
        """
        B (yıldız ile = arasında) içinde sağdan sola taranır,
        ilk bulunan 0/1 (yani henüz x/y'ye dönüşmemiş bit) döner.
        Hiç kalmadıysa None döner.
        """
        ic = self.bant.hucreler
        try:
            yildiz = ic.index("*")
            esit = ic.index("=")
        except ValueError:
            return None
        for i in range(esit - 1, yildiz, -1):
            if ic[i] in ("0", "1"):
                return i
        return None

    # ---- Yardımcı: Sonuç alanına bir binary sayı ekle ----
    def _sonuca_ekle(self, eklenecek: str):
        """
        '=' karakterinden sonraki sonuç alanına 'eklenecek' binary
        sayısını ikili toplama ile ekler. Bu, Turing Makinesinin
        sağa-sola gidip taşıma yöneterek yaptığı işlemin modüler
        özetidir (her adım yine log'a yazılır).
        """
        esit = self.bant.hucreler.index("=")
        # Mevcut sonucu oku
        mevcut = []
        i = esit + 1
        while i < len(self.bant.hucreler) and self.bant.hucreler[i] in ("0", "1"):
            mevcut.append(self.bant.hucreler[i])
            i += 1
        mevcut_str = "".join(mevcut) if mevcut else "0"

        # İkili toplama (en sağ bitten başlayarak, taşımalı)
        toplam = self._binary_topla(mevcut_str, eklenecek)

        # Sonucu banta yaz
        for j in range(esit + 1, len(self.bant.hucreler)):
            self.bant.hucreler[j] = BLANK
        for k, bit in enumerate(toplam):
            self.bant.kafa = esit + 1 + k
            self.bant.yaz(bit)
            self._kaydet(BLANK, bit, "S")  # Sonuca yazma adımı
        # Kafayı = işaretine geri konumlandır
        self.bant.kafa = esit

    @staticmethod
    def _binary_topla(x: str, y: str) -> str:
        """İki binary stringini taşımalı olarak toplar, sonucu string döner."""
        i, j = len(x) - 1, len(y) - 1
        tasima = 0
        sonuc = []
        while i >= 0 or j >= 0 or tasima:
            bx = int(x[i]) if i >= 0 else 0
            by = int(y[j]) if j >= 0 else 0
            s = bx + by + tasima
            sonuc.append(str(s % 2))
            tasima = s // 2
            i -= 1
            j -= 1
        return "".join(reversed(sonuc)) if sonuc else "0"

    # ---- Ana çalıştırma döngüsü ----
    def calistir(self) -> str:
        if self.log:
            print(f"\n>>> Başlangıç bandı: {self.bant.goster()}\n")

        # 1) Bant üzerinde '*' karakterini bul (q_start → q_find_b)
        while self.bant.oku() != "*":
            okunan = self.bant.oku()
            self._kaydet(okunan, okunan, "R")
            self.bant.sag()
        self._kaydet("*", "*", "R")
        self.bant.sag()
        self.durum = "q_find_b"

        # 2) '=' karakterine kadar git (B'nin sağ ucu)
        while self.bant.oku() != "=":
            okunan = self.bant.oku()
            self._kaydet(okunan, okunan, "R")
            self.bant.sag()
        self._kaydet("=", "=", "L")
        self.bant.sol()
        self.durum = "q_scan"

        # 3) B'nin bitlerini sağdan sola sırayla işle
        adim_kayma = 0   # kaç kere sola kaydırıldı
        while True:
            idx = self._sonraki_bit()
            if idx is None:
                # Tüm bitler işlendi
                break

            self.bant.kafa = idx
            bit = self.bant.oku()

            if bit == "1":
                self.durum = "q_bit1"
                # 'y' olarak işaretle
                self.bant.yaz("y")
                self._kaydet("1", "y", "-")
                # A'nın "adim_kayma" kadar sola kaydırılmış halini sonuca ekle
                eklenecek = self.A_orijinal + "0" * adim_kayma
                self.durum = "q_add"
                if self.log:
                    print(f"          >> Sonuca eklenecek: {eklenecek}")
                self._sonuca_ekle(eklenecek)
            else:  # bit == "0"
                self.durum = "q_bit0"
                self.bant.yaz("x")
                self._kaydet("0", "x", "-")

            self.durum = "q_shift"
            adim_kayma += 1

        # 4) Kabul durumu
        self.durum = "q_accept"
        if self.log:
            print(f"\n>>> KABUL. Final bant: {self.bant.icerik()}")

        # Sonucu döndür
        esit = self.bant.hucreler.index("=")
        sonuc = "".join(
            h for h in self.bant.hucreler[esit + 1:] if h in ("0", "1")
        )
        return sonuc or "0"


# ---------------------------------------------------------------
# 3) GİRDİ DOĞRULAMA & ARAYÜZ
# ---------------------------------------------------------------
def gecerli_binary_mi(s: str) -> bool:
    return len(s) > 0 and all(c in "01" for c in s)


def binary_to_decimal(b: str) -> int:
    return int(b, 2) if b else 0


def carp(a: str, b: str, log: bool = True) -> str:
    """Dışarıdan çağırılacak temiz API."""
    if not gecerli_binary_mi(a) or not gecerli_binary_mi(b):
        raise ValueError("Girdiler yalnızca 0 ve 1 içermelidir.")
    tm = TuringMakinesi(a, b, log=log)
    return tm.calistir()


def main():
    print("=" * 60)
    print(" Turing Makinesi ile Binary Çarpma Hesaplayıcı")
    print("=" * 60)

    a = input("Birinci binary sayı: ").strip()
    b = input("İkinci binary sayı : ").strip()

    if not gecerli_binary_mi(a) or not gecerli_binary_mi(b):
        print("HATA: Girdiler yalnızca '0' ve '1' içermelidir.")
        return

    sonuc = carp(a, b, log=True)

    print("\n" + "=" * 60)
    print(f" SONUÇ")
    print("=" * 60)
    print(f" Binary  : {a} × {b} = {sonuc}")
    print(f" Decimal : {binary_to_decimal(a)} × {binary_to_decimal(b)} "
          f"= {binary_to_decimal(sonuc)}")


if __name__ == "__main__":
    main()
