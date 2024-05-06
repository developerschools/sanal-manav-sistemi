import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QComboBox, QPushButton, QVBoxLayout, QTextEdit, QMessageBox, QLineEdit, QDialog, QFormLayout

class KartBilgileriDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Kart Bilgileri")
        self.setGeometry(300, 300, 300, 200)

        self.label_ad = QLabel("Kart Üzerindeki Ad:")
        self.line_edit_ad = QLineEdit()

        self.label_numara = QLabel("Kart Numarası:")
        self.line_edit_numara = QLineEdit()

        self.label_son_kullanma = QLabel("Son Kullanma Tarihi:")
        self.comboBox_yil = QComboBox()
        self.comboBox_ay = QComboBox()

        # Yıl seçeneklerini ekleyelim (2024-2029)
        for yil in range(2024, 2030):
            self.comboBox_yil.addItem(str(yil))

        # Ay seçeneklerini ekleyelim (1-12)
        for ay in range(1, 13):
            self.comboBox_ay.addItem(str(ay))

        self.button_kaydet = QPushButton("Kaydet")
        self.button_kaydet.clicked.connect(self.kaydet_clicked)

        self.layout = QFormLayout()
        self.layout.addRow(self.label_ad, self.line_edit_ad)
        self.layout.addRow(self.label_numara, self.line_edit_numara)
        self.layout.addRow(self.label_son_kullanma, self.comboBox_yil)
        self.layout.addRow("", self.comboBox_ay)
        self.layout.addWidget(self.button_kaydet)

        self.setLayout(self.layout)

    def kaydet_clicked(self):
        kart_numarasi = self.line_edit_numara.text()
        son_kullanma_yil = self.comboBox_yil.currentText()
        son_kullanma_ay = self.comboBox_ay.currentText()

        if len(kart_numarasi) != 16:
            QMessageBox.warning(self, "Uyarı", "Kart numarası 16 haneli olmalıdır.")
        else:
            # Kart bilgilerini veritabanına kaydet
            self.kart_bilgilerini_kaydet(kart_numarasi, son_kullanma_ay, son_kullanma_yil)
            QMessageBox.information(self, "Bilgi", f"Kart Bilgileri Kaydedildi:\n"
                                                    f"Kart Numarası: {kart_numarasi}\n"
                                                    f"Son Kullanma Tarihi: {son_kullanma_ay}/{son_kullanma_yil}")

    def kart_bilgilerini_kaydet(self, kart_numarasi, son_kullanma_ay, son_kullanma_yil):
        try:
            # Veritabanı bağlantısını oluştur
            con = sqlite3.connect("kart_bilgileri.db")
            cur = con.cursor()

            # Tablo oluştur (ilk çalıştırmada bir kere)
            cur.execute('''CREATE TABLE IF NOT EXISTS kartlar (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            kart_numarasi TEXT NOT NULL,
                            son_kullanma_ay TEXT NOT NULL,
                            son_kullanma_yil TEXT NOT NULL
                            )''')

            # Kart bilgilerini ekle
            cur.execute("INSERT INTO kartlar (kart_numarasi, son_kullanma_ay, son_kullanma_yil) VALUES (?, ?, ?)",
                        (kart_numarasi, son_kullanma_ay, son_kullanma_yil))
            
            # Değişiklikleri kaydet ve bağlantıyı kapat
            con.commit()
            con.close()
        except Exception as e:
            QMessageBox.warning(self, "Hata", f"Kart bilgileri kaydedilirken bir hata oluştu:\n{str(e)}")

class SanalManavArayuz(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

        # Sepet bilgileri
        self.sepet = {}

    def init_ui(self):
        self.setWindowTitle("Sanal Manav")
        self.setGeometry(100, 100, 600, 500)

        self.label_urun_adi = QLabel("Ürün Adı:")
        self.comboBox_urun_adi = QComboBox()
        self.comboBox_urun_adi.addItems([
            "Salkım Domates", "Yerli Muz", "İthal Muz", "Salatalık", "Havuç", "Portakal", 
            "Sakız Kabağı", "Sıkma Portakal",  "Çilek", "Kırmızı Biber", "Domates", 
            "Patlıcan", "Çarliston Biber", "Kivi", "Sivri Biber", "Kırmızı Elma", "Yeşil Elma", 
            "Armut", "Fasulye", "Bezelye", "Tatlı Patates", "Kuru Soğan", "Kırmızı Soğan", "Patates"
        ])

        self.label_miktar = QLabel("Ürün Miktarı (Kilogram):")
        self.comboBox_miktar = QComboBox()
        self.comboBox_miktar.addItems(["1 Kilogram", "2 Kilogram", "3 Kilogram", "4 Kilogram", "5 Kilogram", "6 Kilogram", "7 Kilogram", "8 Kilogram", "9 Kilogram", "10 Kilogram"])

        self.label_kilogram_fiyati = QLabel("Kilogram Fiyatı:")
        self.label_kilogram_fiyati_sonuc = QLabel("")

        self.button_kilogram_fiyati = QPushButton("Kilogram Fiyatı Göster")
        self.button_kilogram_fiyati.clicked.connect(self.kilogram_fiyati_goster_clicked)

        self.button_sepete_ekle = QPushButton("Sepete Ekle")
        self.button_sepete_ekle.clicked.connect(self.sepete_ekle_clicked)

        self.button_sepeti_goster = QPushButton("Sepeti Göster")
        self.button_sepeti_goster.clicked.connect(self.sepeti_goster_clicked)

        self.textEdit_sepet = QTextEdit()

        self.label_adres = QLabel("Adres Bilgileri:")
        self.label_il = QLabel("İl:")
        self.line_edit_il = QLineEdit()
        self.line_edit_il.setText("İstanbul")  # Default olarak İstanbul'u ayarla
        self.label_ilce = QLabel("İlçe:")
        self.line_edit_ilce = QLineEdit()
        self.line_edit_ilce.setText("Sultangazi")  # Default olarak Sultangazi'yi ayarla
        self.label_mahalle = QLabel("Mahalle:")
        self.comboBox_mahalle = QComboBox()
        self.comboBox_mahalle.addItems([
            "50. Yıl", "75. Yıl", "Cebeci", "Cumhuriyet", "Esentepe", "Eski Habibler", 
            "Gazi", "Habibler", "İsmetpaşa", "Malkoçoğlu", "Sultançiftliği", "Uğur Mumcu", 
            "Yayla", "Yunusemre", "Zübeydehanım"
        ])
        self.label_sokak = QLabel("Sokak:")
        self.line_edit_sokak = QLineEdit()
        self.label_no = QLabel("No:")
        self.line_edit_no = QLineEdit()
        self.label_daire = QLabel("Daire:")
        self.line_edit_daire = QLineEdit()

        self.label_odeme_yontemi = QLabel("Ödeme Yöntemi:")
        self.comboBox_odeme_yontemi = QComboBox()
        self.comboBox_odeme_yontemi.addItems(["Nakit", "Banka/Kredi Kartı"])
        self.comboBox_odeme_yontemi.currentIndexChanged.connect(self.odeme_yontemi_degisti)

        self.button_siparisi_tamamla = QPushButton("Siparişi Tamamla")
        self.button_siparisi_tamamla.clicked.connect(self.siparisi_tamamla_clicked)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.label_urun_adi)
        self.layout.addWidget(self.comboBox_urun_adi)
        self.layout.addWidget(self.label_miktar)
        self.layout.addWidget(self.comboBox_miktar)
        self.layout.addWidget(self.label_kilogram_fiyati)
        self.layout.addWidget(self.label_kilogram_fiyati_sonuc)
        self.layout.addWidget(self.button_kilogram_fiyati)
        self.layout.addWidget(self.button_sepete_ekle)
        self.layout.addWidget(self.button_sepeti_goster)
        self.layout.addWidget(self.textEdit_sepet)
        self.layout.addWidget(self.label_adres)
        self.layout.addWidget(self.label_il)
        self.layout.addWidget(self.line_edit_il)
        self.layout.addWidget(self.label_ilce)
        self.layout.addWidget(self.line_edit_ilce)
        self.layout.addWidget(self.label_mahalle)
        self.layout.addWidget(self.comboBox_mahalle)
        self.layout.addWidget(self.label_sokak)
        self.layout.addWidget(self.line_edit_sokak)
        self.layout.addWidget(self.label_no)
        self.layout.addWidget(self.line_edit_no)
        self.layout.addWidget(self.label_daire)
        self.layout.addWidget(self.line_edit_daire)
        self.layout.addWidget(self.label_odeme_yontemi)
        self.layout.addWidget(self.comboBox_odeme_yontemi)
        self.layout.addWidget(self.button_siparisi_tamamla)

        self.setLayout(self.layout)

    def odeme_yontemi_degisti(self, index):
        if index == 1:  # Eğer "Banka/Kredi Kartı" seçildiyse
            self.kart_bilgileri_dialog = KartBilgileriDialog(self)
            self.kart_bilgileri_dialog.exec_()

    def kilogram_fiyati_goster_clicked(self):
        secilen_urun = self.comboBox_urun_adi.currentText()
        secilen_miktar = self.comboBox_miktar.currentText().split()[0]  # Sadece miktarı almak için
        kilogram_fiyati = self.get_kilogram_fiyati(secilen_urun)
        if kilogram_fiyati is not None:
            toplam_fiyat = float(secilen_miktar) * kilogram_fiyati
            self.label_kilogram_fiyati_sonuc.setText("{} Kilogram için Toplam Fiyat: {} TL".format(secilen_miktar, toplam_fiyat))
        else:
            self.label_kilogram_fiyati_sonuc.setText("Bulunamadı")

    def sepete_ekle_clicked(self):
        secilen_urun = self.comboBox_urun_adi.currentText()
        secilen_miktar = self.comboBox_miktar.currentText()
        if secilen_urun in self.sepet:
            self.sepet[secilen_urun] += float(secilen_miktar.split()[0])
        else:
            self.sepet[secilen_urun] = float(secilen_miktar.split()[0])
        self.label_kilogram_fiyati_sonuc.setText("{} sepete eklendi.".format(secilen_urun + " - " + secilen_miktar))

    def sepeti_goster_clicked(self):
        sepet_listesi = ""
        toplam_fiyat = 0
        for urun, miktar in self.sepet.items():
            fiyat = self.get_kilogram_fiyati(urun)
            toplam_fiyat += fiyat * miktar
            sepet_listesi += "{} - {} Kilogram\n".format(urun, miktar)
        sepet_listesi += "Toplam Fiyat: {} TL".format(toplam_fiyat)
        self.textEdit_sepet.setText(sepet_listesi)

    def siparisi_tamamla_clicked(self):
        il = self.line_edit_il.text()
        ilce = self.line_edit_ilce.text()
        mahalle = self.comboBox_mahalle.currentText()
        sokak = self.line_edit_sokak.text()
        no = self.line_edit_no.text()
        daire = self.line_edit_daire.text()
        odeme_yontemi = self.comboBox_odeme_yontemi.currentText()

        if il and ilce and mahalle and sokak and no and daire and odeme_yontemi:
            adres_bilgisi = f"Adres: {il} / {ilce} / {mahalle} Mah. / {sokak} Sok. No: {no} / Daire: {daire}"
            toplam_fiyat = self.hesapla_toplam_fiyat()
            QMessageBox.information(self, "Sipariş Bilgileri", f"{adres_bilgisi}\n"
                                                                f"Ödeme Yöntemi: {odeme_yontemi}\n"
                                                                f"Toplam Tutar: {toplam_fiyat} TL\n\n"
                                                                f"Siparişiniz başarıyla alınmıştır. Bizi tercih ettiğiniz için teşekkür ederiz.")
        else:
            QMessageBox.warning(self, "Uyarı", "Lütfen tüm bilgileri eksiksiz giriniz.")

    def hesapla_toplam_fiyat(self):
        toplam_fiyat = 0
        for urun, miktar in self.sepet.items():
            fiyat = self.get_kilogram_fiyati(urun)
            toplam_fiyat += fiyat * miktar
        return toplam_fiyat

    def get_kilogram_fiyati(self, urun_adi):
        kilogram_fiyatlari = {
            "Salkım Domates": 40.00,
            "Yerli Muz": 50.50,
            "İthal Muz": 80.25,
            "Salatalık": 22.25,
            "Havuç": 43.750,
            "Portakal": 25.00,
            "Sakız Kabağı": 36.00,
            "Sıkma Portakal": 23.50,
            
            "Çilek": 60.00,
            "Kırmızı Biber": 95.75,
            "Domates": 30.00,
            "Patlıcan": 23.00,
            "Çarliston Biber": 25.50,
            "Kivi": 90.25,
            "Sivri Biber": 40.00,
            "Kırmızı Elma": 20.75,
            "Yeşil Elma": 20.50,
            "Armut": 50.25,
            "Fasulye": 80.75,
            "Bezelye": 30.50,
            "Tatlı Patates": 110.00,
            "Kuru Soğan": 15.25,
            "Kırmızı Soğan": 50.50,
            "Patates": 18.00
        }
        return kilogram_fiyatlari.get(urun_adi)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    arayuz = SanalManavArayuz()
    arayuz.show()
    sys.exit(app.exec_())
