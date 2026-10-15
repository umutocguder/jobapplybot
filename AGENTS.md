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

---

## Git Branch Model — `master` = production, `dev` = UAT  (MANDATORY)

Set by Umut on 2026-10-15. **This overrides any earlier branch or tagging
instruction in this file**, including "auto-bump and tag on every push".

| Branch | Meaning | Rule |
|---|---|---|
| `master` | **Production** — what is live / shipped right now | Never commit directly. Only released code is merged in. |
| `dev` | **UAT** — where development happens; always ahead of or equal to `master` | All work lands here. |

The branch name `main` is not used.

**The agent manages branch switching, commits, merges and tags itself — it does
not ask Umut which branch to work on.**

1. A code change is requested → if on `master`, **switch to `dev` immediately**.
   The change and the commit go to `dev`.
2. Builds and packages are produced from `dev`.
3. The moment it goes live — App Store approval, Vercel production, delivery to
   the client — merge `dev` into `master`.
4. Tag on `master`: `v<version>` (e.g. `v1.0`, `v1.1`). **A tag is only ever
   created for a version that actually shipped.** Never tag on every push.
5. Development continues on `dev`. After the merge, `dev` and `master` are equal.

If a merge conflict appears, stop and tell Umut — do not resolve it alone.

Full rule: `/Users/umut/ai-context/kurallar/git-dal-modeli-master-dev.md`
