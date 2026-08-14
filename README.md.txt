# 🖥️ Real-Time System Performance & Task Monitor (Python GUI)

Bu proje, bilgisayarın CPU ve RAM kaynak kullanımını gerçek zamanlı olarak izleyen, dinamik grafiklerle görselleştiren ve arka planda çalışan süreçleri analiz eden Python tabanlı bir masaüstü uygulamasıdır.

---

## 📸 Ekran Görüntüsü

![Uygulama Ekranı](preview.png)

---

## 🚀 Temel Özellikler

* **Gerçek Zamanlı Metrikler:** `psutil` kütüphanesi ile anlık CPU ve RAM kullanım oranlarının takibi.
* **Dinamik Veri Görselleştirme:** Matplotlib kullanılarak son 50 saniyelik verinin kayan pencereli (sliding window) grafikler üzerinde gösterimi; anlık ortalama, maksimum ve minimum referans çizgileri.
* **Süreç & Görev Takibi:** Çalışan aktif işlemlerin PID, süreç adı, anlık CPU yüzdesi ve bellek tüketimi (MB) bazında dinamik tablolaması (`ttk.Treeview`).
* **Değişim Vurgulama:** Süreçlerin bellek kullanımındaki anlık değişimlerin görsel olarak renklendirilmesi.

---

## 🛠️ Kullanılan Teknolojiler

* **Python 3**
* **Tkinter & ttk:** Masaüstü kullanıcı arayüzü ve tablo bileşenleri
* **Matplotlib (`FigureCanvasTkAgg`):** Gömülü dinamik grafikler
* **psutil:** Sistem kaynakları ve süreç yönetimi
* **NumPy:** Sayısal veri kaydırma ve istatistiksel hesaplamalar
* **Pillow (PIL):** Arayüz görsel yönetimi

---

## ⚙️ Kurulum ve Çalıştırma


1. Repoyu klonlayın:
```bash
git clone https://github.com/selengull/realtime-system-performance-monitor.git
cd realtime-system-performance-monitor

2. Gerekli kütüphaneleri yükleyin:
pip install -r requirements.txt

3. Uygulamayı başlatın:
python main.py

