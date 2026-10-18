# JobApplyBot 💼⚡

> **Created by 11Hopem**  
> *Otonom CV Eşleme, ATS Anahtar Kelime Analizi, İlan Radarı ve Freelance Teklif Motoru.*

![JobApplyBot Logo](assets/logo.svg)

---

## 🎯 Özellikler
- **Uzaktan İlan Radarı (Job Radar):** WeWorkRemotely, RemoteOK ve doğrulanmış ilan kaynaklarını tarar, ilanları çeker ve filtreler.
- **ATS Uyumluluk & Anahtar Kelime Analizi:** İlan metnini adayın CV'siyle karşılaştırarak semantik uyumluluk puanı (Match Score %) hesaplar, eksik yetkinlikleri listeler.
- **Kişiselleştirilmiş Teklif & Cover Letter Üreteci:** İlanın gereksinimlerine göre Upwork/Bionluk freelance teklifleri veya kurumsal iş başvurusu ön yazıları üretir (Türkçe & İngilizce).
- **Başvuru Takip Defteri (Tracker):** Başvurulan pozisyonları, mülakat aşamalarını ve teklifleri yerel diskte güvenle saklar.
- **Otonom Yedekleme & SHA-256 Denetimi:** Her başvuru işleminde otomatik anlık JSON yedeği alır ve bütünlük kontrolü yapar.
- **Sıfır Dış Bağımlılık (Zero External Dependency):** Harici paket kurulumuna ihtiyaç duymadan %100 Python 3 standart kütüphanesiyle çalışır.

---

## 🛠️ Hızlı Başlangıç & CLI Komutları

Botu doğrudan CLI üzerinden veya `scripts/jobhunter.py` betiğiyle çalıştırabilirsiniz:

```bash
# 1. Aday profilini ve yetenekleri görüntüleme
python3 -m jobapplybot profile

# 2. İlan radarı ile uygun fırsatları tarama ve puanlama
python3 -m jobapplybot scan --keywords "ios,swift,mobile" --limit 5

# 3. İlan metnine özel ATS uyumluluk analizi yapma
python3 -m jobapplybot match --text "Looking for Senior Swift iOS developer with UIKit knowledge."

# 4. İlana nokta atışı freelance teklif (Proposal) üretme (Türkçe veya İngilizce)
python3 -m jobapplybot propose --title "Senior iOS Engineer" --company "Fintech Corp" --type freelance --lang tr

# 5. Kurumsal iş başvurusu için Cover Letter üretme
python3 -m jobapplybot propose --title "Lead Mobile Engineer" --company "Stripe" --type corporate --lang en

# 6. Yapılan başvuruyu takip defterine kaydetme
python3 -m jobapplybot apply --company "Apple" --position "iOS Engineer" --score 85.0 --url "https://jobs.apple.com"

# 7. Başvuru hunisi ve istatistik raporunu görüntüleme
python3 -m jobapplybot status
```

---

## 🧪 Testleri Çalıştırma
```bash
python3 -m unittest discover -s tests
```
