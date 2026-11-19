"""What each team feature is expected to do. The placeholder screens and the home page are built from this list.

When a student finishes a feature, its screen in ``views/`` stops calling ``render_placeholder`` and shows the real
feature. Keep the texts here up to date if the agreed behaviour changes.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Feature:
    key: str
    title: str
    owner: str
    module: str
    view: str
    acceptance_test: str
    summary: str
    expected: tuple[str, ...]
    acceptance: tuple[str, ...]


FEATURES: tuple[Feature, ...] = (
    Feature(
        key="plan",
        title="Seviye testi ve kişisel plan",
        owner="Arda Tözün",
        module="repquest/plan_generator.py",
        view="views/level_test_plan.py",
        acceptance_test="tests/acceptance/test_plan_generator.py",
        summary="Kısa bir fitness seviye testi ve sonuca göre kişisel antrenman planı.",
        expected=(
            "Aktif profil kısa bir seviye testini doldurur. Örnek sorular: şınav ve squat tekrarı, plank süresi, "
            "haftada kaç gün antrenman yapılabileceği.",
            "Test sonucu fitness seviyesini belirler: `beginner`, `intermediate` veya `advanced`.",
            "Plan, fitness seviyesi ve haftalık gün sayısına göre üretilir. Plandaki egzersizler kütüphanedeki "
            "`exercise_id` değerleriyle belirtilir.",
            "Fitness seviyesi, XP'den gelen oyun seviyesinden ayrı saklanır. XP fitness seviyesini değiştirmez.",
        ),
        acceptance=(
            "Aynı test cevapları aynı fitness seviyesini verir.",
            "Üretilen plandaki her `exercise_id` egzersiz kütüphanesinde bulunur.",
        ),
    ),
    Feature(
        key="library",
        title="Egzersiz kütüphanesi",
        owner="Ferhat Altunel",
        module="repquest/exercise_library.py",
        view="views/exercise_library.py",
        acceptance_test="tests/acceptance/test_exercise_library.py",
        summary="Egzersiz listesi, ada göre arama ve kas grubuna göre filtreleme.",
        expected=(
            "Her egzersizin kalıcı bir `exercise_id` değeri vardır. Ekranda görünen ad kimlik olarak kullanılmaz.",
            "Ada göre arama büyük/küçük harfe duyarsızdır. Kas grubu filtresi `contracts.MUSCLE_GROUPS` "
            "kimliklerini kullanır.",
            "Kişisel plan ve antrenman kaydı egzersizleri bu kütüphaneden seçer.",
            "Workout A egzersizleri (`bench_press`, `dumbbell_row`, `squat`) kütüphanede aynı kimliklerle bulunur.",
        ),
        acceptance=(
            "`press` araması Bench Press'i bulur.",
            "`back` filtresi Dumbbell Row'u gösterir, Squat'ı göstermez.",
        ),
    ),
    Feature(
        key="logger",
        title="Antrenman kaydı, geçmiş ve seri",
        owner="Judith Ilunga",
        module="repquest/workout_logger.py",
        view="views/workout_log.py",
        acceptance_test="tests/acceptance/test_workout_logger.py",
        summary="Set set antrenman kaydı, tamamlanan antrenmanların geçmişi ve günlük seri.",
        expected=(
            "Antrenman bir şablondan (ör. `workout_a`) ya da kütüphaneden seçilen egzersizlerle başlar. "
            "Her set için ağırlık (kg) ve tekrar sayısı kaydedilir.",
            "Antrenman tamamlandığında yeni bir `workout_id` oluşur. Şablonun `template_id` değeri ayrı kalır, "
            "şablon değişmez.",
            "Geçmiş, aktif profilin tamamlanan antrenmanlarını yeniden eskiye gösterir.",
            "Seri, art arda antrenman yapılan günleri sayar. Aynı gün yapılan ikinci antrenman seriyi artırmaz.",
        ),
        acceptance=(
            "Workout A'dan başlatılıp tamamlanan antrenman geçmişte yeni bir `workout_id` ile görünür.",
            "Aynı gün iki antrenman kaydedilince seri yalnızca bir kez artar.",
        ),
    ),
    Feature(
        key="gamification",
        title="XP, oyun seviyesi ve avatar",
        owner="Duru Göktaş",
        module="repquest/gamification.py",
        view="views/progress_avatar.py",
        acceptance_test="tests/acceptance/test_gamification.py",
        summary="Tamamlanan antrenmanlardan XP, XP'den oyun seviyesi ve seviyeyle gelişen avatar.",
        expected=(
            "Tamamlanan her antrenman, kurallara göre XP verir. Örnek kural: tamamlanan set başına sabit XP.",
            "Toplam XP'den oyun seviyesi hesaplanır. Oyun seviyesi fitness seviyesinden ayrıdır.",
            "Aynı `workout_id` ikinci kez XP vermez.",
            "Avatar oyun seviyesine göre aşama aşama gelişir.",
        ),
        acceptance=(
            "Aynı `workout_id` için XP iki kez istenirse toplam XP değişmez.",
            "XP eşiği geçilince oyun seviyesi ve avatar aşaması artar, fitness seviyesi değişmez.",
        ),
    ),
    Feature(
        key="social",
        title="Arkadaşlar ve haftalık sıralama",
        owner="Kelvin Chukwukelu",
        module="repquest/social.py",
        view="views/friends_leaderboard.py",
        acceptance_test="tests/acceptance/test_social.py",
        summary="İki demo profil arasında arkadaşlık ve seçili haftanın XP'sine göre sıralama.",
        expected=(
            "Aktif profil diğer demo profile arkadaşlık isteği gönderir. Diğer profil isteği kabul edince "
            "arkadaşlık oluşur.",
            "Haftalık sıralama seçili haftada (pazartesi–pazar) kazanılan XP'yi kullanır, toplam XP'yi kullanmaz.",
            "Sıralamada aktif profil ve arkadaşları görünür.",
        ),
        acceptance=(
            "Deniz ve Ece arkadaş olunca ikisi de birbirinin sıralamasında görünür.",
            "Önceki haftada kazanılan XP seçili haftanın sıralamasını değiştirmez.",
        ),
    ),
    Feature(
        key="database",
        title="Veritabanı ve entegrasyon",
        owner="Mehmet Arif Yörük",
        module="repquest/db.py",
        view="views/database.py",
        acceptance_test="tests/acceptance/test_end_to_end.py",
        summary="SQLite ürün tabloları, ilişkiler ve modüllerin tek akışta birleşmesi.",
        expected=(
            "Ürün tablolarını ve ilişkilerini tasarlar: profiller, egzersizler, şablonlar, tamamlanan antrenmanlar, "
            "setler, XP olayları, arkadaşlıklar.",
            "Kurulum boş bir veritabanı dosyasında çalışır ve tekrar çalıştırılabilir.",
            "Modülleri birleştirir. Tam akış: seviye testi → plan → egzersiz seçimi → antrenman kaydı → geçmiş "
            "ve seri → XP ve avatar → haftalık sıralama.",
        ),
        acceptance=(
            "Boş bir veritabanında iki demo profille tam akış uçtan uca çalışır.",
        ),
    ),
)

_BY_KEY = {feature.key: feature for feature in FEATURES}


def feature(key: str) -> Feature:
    """The feature with ``key``. Raises KeyError for an unknown key."""
    return _BY_KEY[key]
