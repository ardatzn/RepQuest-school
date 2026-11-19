# RepQuest School

**Antrenman yap → kaydet → ilerleme kazan → avatarın gelişsin.**

Bu depo, mevcut RepQuest Android uygulamasından uyarlanmış bir **okul projesi iskeletidir**. Python, Streamlit ve
SQLite kullanır. Android kodu, geçmişi ve verisi bu depoda yoktur. Bu sürüm yalnızca açılabilen bir ana ekran, iki
kurgusal demo profil, salt okunur Workout A örneği, SQLite başlangıç kurulumu ve altı öğrencinin geliştireceği
modüllerin yer tutucu ekranlarını içerir.

## Kurulum

Python 3.10 veya üstü gerekir.

```bash
git clone https://github.com/ardatzn/RepQuest-school.git
cd RepQuest-school
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Ubuntu/Debian'da `python3 -m venv` hata verirse önce `sudo apt install python3-venv` çalıştır.

## Çalıştırma

```bash
streamlit run app.py
```

Tarayıcıda `http://localhost:8501` açılır. Aktif demo profil kenar çubuğundan seçilir ve oturum boyunca bütün
ekranlarda kalır.

İlk açılışta `data/repquest_school.db` oluşturulur. Bu dosya yereldir ve Git'e eklenmez. Başka bir dosya kullanmak
için `REPQUEST_DB_PATH=/yol/dosya.db streamlit run app.py` çalıştır. Sıfırdan başlamak için `data/` klasörünü sil.

## Testler

```bash
pytest
```

`tests/test_*.py` iskeletin kendisini test eder. `tests/acceptance/` altındaki kabul senaryoları şimdilik
atlanmış (skip) durumdadır. Her öğrenci kendi dosyasındaki `skip` satırını kaldırıp gerçek senaryoyu yazar.

## Dosya yapısı

```
app.py                      Giriş noktası: SQLite kurulumu, profil seçici, sayfa gezinmesi
repquest/
  contracts.py              Ortak veri sözleşmesi (kimlikler, kas grupları, fitness seviyeleri)
  demo_data.py              İki demo profil ve Workout A (salt okunur)
  db.py                     SQLite bağlantısı ve başlangıç kurulumu
  session.py                Aktif demo profil (Streamlit oturumu)
  features.py               Her modülün beklenen davranışı (yer tutucu ekranlar bunu gösterir)
  ui.py                     Yer tutucu ekran yardımcısı
  plan_generator.py         ┐
  exercise_library.py       │
  workout_logger.py         ├ Öğrenci modülleri (şimdilik NotImplementedError)
  gamification.py           │
  social.py                 ┘
views/                      Ekranlar (her öğrencinin kendi ekran dosyası var)
tests/                      İskelet testleri ve tests/acceptance/ kabul senaryoları
```

## Görev dağılımı

| Öğrenci | Sorumluluk | Modül | Ekran | Kabul testi |
|---|---|---|---|---|
| Mehmet Arif Yörük | Mimari, SQLite veri tasarımı ve entegrasyon | `repquest/db.py` ve ortak altyapı | `views/database.py` | `tests/acceptance/test_end_to_end.py` |
| Arda Tözün | Fitness seviye testi ve kişisel antrenman planı | `repquest/plan_generator.py` | `views/level_test_plan.py` | `tests/acceptance/test_plan_generator.py` |
| Ferhat Altunel | Egzersiz kütüphanesi, arama ve filtreleme | `repquest/exercise_library.py` | `views/exercise_library.py` | `tests/acceptance/test_exercise_library.py` |
| Judith Ilunga | Antrenman ve set kaydı, geçmiş ve seri | `repquest/workout_logger.py` | `views/workout_log.py` | `tests/acceptance/test_workout_logger.py` |
| Duru Göktaş | XP, oyun seviyesi ve avatar ilerlemesi | `repquest/gamification.py` | `views/progress_avatar.py` | `tests/acceptance/test_gamification.py` |
| Kelvin Chukwukelu | Arkadaşlar ve haftalık sıralama | `repquest/social.py` | `views/friends_leaderboard.py` | `tests/acceptance/test_social.py` |

Modül dosyalarındaki fonksiyon imzaları birer öneridir. İmzayı değiştiren PR, o fonksiyonu kullanan modüllerin
sahiplerine de inceletilir.

## Hazır olanlar ve öğrencilere kalanlar

Hazır:

- Ana ekran, iki kurgusal demo profil (`demo_deniz`, `demo_ece`) ve oturumda tutulan aktif profil.
- Salt okunur Workout A: Bench Press, Dumbbell Row ve Squat, üçer set. Kimlikler Android uygulamasıyla aynıdır.
- SQLite bağlantısı ve boş bir dosyada çalışan, tekrar çalıştırılabilir kurulum. Şimdilik yalnızca `schema_meta`
  tablosu var.
- Her modül için açılabilen yer tutucu ekran, beklenen davranış ve örnek kabul senaryoları.

Öğrencilere kalan:

- Ürün tabloları, ilişkiler ve modül entegrasyonu (Mehmet Arif).
- Seviye testi ve plan üretme (Arda).
- Egzersiz listesi, arama ve filtreleme (Ferhat).
- Antrenman ve set kaydı, geçmiş ve seri (Judith).
- XP, oyun seviyesi ve avatar (Duru).
- Arkadaşlık ve haftalık sıralama (Kelvin).

## Ortak veri sözleşmesi

Ortak kimlikler ve kurallar `repquest/contracts.py` dosyasındadır. Bunları değiştiren bir PR'ı bütün modül sahipleri
inceler.

| Kimlik | Tür | Örnek | Anlamı |
|---|---|---|---|
| `user_id` | TEXT | `demo_deniz` | Profil. Bu projede yalnızca kurgusal demo profiller var. |
| `exercise_id` | TEXT, `^[a-z0-9_]{1,64}$` | `bench_press` | Kütüphanedeki egzersizin kalıcı kimliği. Görünen ad kimlik değildir. |
| `template_id` | TEXT | `workout_a` | Workout A gibi tekrar kullanılabilir şablon. Şablon tamamlanmış bir antrenman değildir. |
| `workout_id` | TEXT, `uuid.uuid4().hex` | `3f2a…` | Tamamlanmış tek bir antrenman. Yalnızca antrenman bitince oluşur. |

Diğer kurallar:

- **Tarih:** antrenman tarihi yerel gün olarak `YYYY-MM-DD` biçimindedir.
- **Hafta:** pazartesi–pazar. Bir hafta, pazartesi tarihiyle (`week_start`, `YYYY-MM-DD`) tanımlanır.
- **Kas grupları:** `chest`, `back`, `legs`, `shoulders`, `arms`, `core`.
- **Fitness seviyesi:** seviye testinden gelir: `beginner`, `intermediate` veya `advanced`.
- **Oyun seviyesi:** yalnızca XP'den hesaplanır. Fitness seviyesi ile oyun seviyesi ayrı tutulur ve birbirini
  değiştirmez.
- **XP:** tamamlanan `workout_id` başına verilir. Aynı `workout_id` ikinci kez XP vermez. Her XP kaydı kazanıldığı
  tarihi saklar.
- **Seri:** art arda antrenman yapılan günleri sayar. Aynı gün yapılan ikinci antrenman seriyi tekrar artırmaz.
- **Haftalık sıralama:** seçili haftada kazanılan XP'ye göre yapılır, toplam XP'ye göre yapılmaz.
- **Demo:** arkadaşlık ve sıralama iki demo profille (`demo_deniz`, `demo_ece`) gösterilebilir olmalıdır.

## Tamamlanmış akış

Ekip bittiğinde uygulama şu akışı uçtan uca çalıştırır:

1. Seviye testi → fitness seviyesi (Arda)
2. Kişisel plan (Arda)
3. Plandan ya da kütüphaneden egzersiz seçimi (Ferhat)
4. Antrenman ve set kaydı → yeni `workout_id` (Judith)
5. Geçmiş ve seri (Judith)
6. XP, oyun seviyesi ve avatar (Duru)
7. Haftalık sıralama (Kelvin)

Bütün veriler Mehmet Arif'in tasarladığı SQLite tablolarında tutulur. Uçtan uca senaryo
`tests/acceptance/test_end_to_end.py` dosyasında yazılır.

## Çalışma akışı: feature branch → PR

`main` dalına doğrudan push yapılmaz. Her iş kendi dalında yapılır ve PR ile birleştirilir.

```bash
git switch main
git pull
git switch -c feature/<isim>-<konu>      # ör. feature/ferhat-exercise-library
# modülünü, ekranını ve kabul testini yaz
pytest
git add <değişen dosyalar>
git commit -m "Egzersiz araması ve kas grubu filtresi"
git push -u origin feature/<isim>-<konu>
gh pr create --base main --fill          # ya da GitHub web arayüzünden PR aç
```

Her öğrencinin PR'ı:

- kendi modülünü, kendi ekranını ve en az bir çalışan kabul senaryosunu içerir;
- `pytest` çıktısının geçtiğini gösterir;
- ortak sözleşmeyi (`repquest/contracts.py`) değiştiriyorsa bunu açıklamada belirtir;
- Mehmet Arif (entegrasyon) ve en az bir ekip arkadaşı tarafından incelenip onaylandıktan sonra birleştirilir.

`main` ile çakışma olursa dalında `git pull origin main` çalıştır, çakışmayı çöz ve testleri tekrar çalıştır.

## Veri ve gizlilik

Bu projede gerçek kullanıcı verisi kullanılmaz. Demo profiller kurgusaldır. Yerel veritabanı (`data/`), `.env` ve
`.streamlit/secrets.toml` Git'e eklenmez.
