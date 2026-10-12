# JobApplyBot — Development & Architectural Guidelines

Bu doküman, **JobApplyBot** otonom iş başvuru, CV eşleme ve kariyer takip sisteminin mimari standartlarını ve geliştirme kurallarını belirler.

---

## 1. Proje Kimliği ve Amacı
- **Proje Adı**: JobApplyBot
- **Amaç**: Adayların CV'lerini iş ilanlarıyla otomatik eşleyen, ATS (Aday Takip Sistemi) anahtar kelime uyumluluğunu hesaplayan ve başvuru süreçlerini güvenle takip eden kariyer otomasyon aracı.
- **Geliştirici**: Umut Öçgüder <umutocgdr@gmail.com> / 11Hopem
- **Logo Varlığı**: `assets/logo.svg`

---

## 2. Mimari ve Teknoloji Yığını
- **Dil**: Python 3.10+ (Standard Library, zero external dependency)
- **Veri Saklama**: %100 Local Data Custody (JSON / SQLite)
- **Telemetri**: Dual-tier `jobapplybot.logger` (Yerel JSONL + Firebase Cloud Logging `hopem-software-cloud`)
- **Telif**: Her dosyada `Created by 11Hopem`

---

## 3. Test ve Çalıştırma
- **Testleri Koşturma**: `python3 -m unittest discover -s tests`
