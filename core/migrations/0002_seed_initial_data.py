from datetime import date, time

from django.db import migrations

INITIAL_POSTS = [{'slug': 'first-tables-soon', 'image': 'assets/images/restaurant-hero-table.png', 'date': '2026-06-17', 'status': 'published', 'title': {'en': 'First Tables Soon', 'jp': 'まもなく最初のテーブルへ', 'ru': 'Первые столы уже скоро', 'uz': 'Birinchi stollar tez orada'}, 'summary': {'en': 'Opening notes, hours, and what to expect when you visit.', 'jp': '営業時間、ご来店前に知っておきたいことをお知らせします。', 'ru': 'Заметки об открытии, часы работы и что ждать от первого визита.', 'uz': "Ochilish eslatmalari, ish vaqti va tashrif oldidan bilish kerak bo'lganlar."}, 'content': {'en': 'We are preparing the first tables for Jingisukan Izakaya in Yunusabad. Expect warm light, lamb on the grill, vegetables over the heat, and a relaxed izakaya mood. Follow our social channels for opening updates and reservation news.', 'jp': 'ユヌサバードで、じんぎすかん居酒屋の最初のテーブルを準備しています。温かい灯り、鉄板で焼くラムと野菜、ゆったりした居酒屋の雰囲気をお楽しみください。オープン情報と予約のお知らせはSNSで更新します。', 'ru': 'Мы готовим первые столы Jingisukan Izakaya в Юнусабаде. Вас ждут теплый свет, баранина на гриле, овощи на жаре и спокойная атмосфера изакаи. Следите за соцсетями, чтобы узнать новости открытия и бронирования.', 'uz': "Yunusobodda Jingisukan Izakaya uchun birinchi stollarni tayyorlayapmiz. Sizni iliq yorug'lik, grilda qo'y go'shti, olov ustidagi sabzavotlar va sokin izakaya kayfiyati kutadi. Ochilish va band qilish yangiliklari uchun ijtimoiy tarmoqlarimizni kuzating."}}, {'slug': 'before-you-come', 'image': 'assets/images/restaurant-hero.png', 'date': '2026-06-17', 'status': 'published', 'title': {'en': 'Before You Come', 'jp': 'ご来店前に', 'ru': 'Перед визитом', 'uz': 'Kelishdan oldin'}, 'summary': {'en': 'Find us in Yunusabad and choose a comfortable time for the grill.', 'jp': 'タシュケント、ユヌサバードでお待ちしています。', 'ru': 'Найдите нас в Юнусабаде и выберите удобное время для гриля.', 'uz': 'Bizni Yunusoboddan toping va gril uchun qulay vaqtni tanlang.'}, 'content': {'en': 'Jingisukan is best enjoyed slowly. Come with friends, choose lamb and sides, then grill at the table. The restaurant is located at Chingiz Aytmatov 44 in Yunusabad, Tashkent.', 'jp': 'ジンギスカンは、ゆっくり楽しむのがおすすめです。友人と一緒に来て、ラムと小皿を選び、テーブルで焼いてお召し上がりください。店舗はタシュケント市ユヌサバード地区、チンギズ・アイトマトフ44番地です。', 'ru': 'Джингисукан лучше всего есть неспешно. Приходите с друзьями, выбирайте баранину и закуски, затем жарьте прямо за столом. Ресторан находится по адресу Чингиза Айтматова 44, Юнусабад, Ташкент.', 'uz': "Jingisukanni sekin, suhbat bilan yeyish yaxshi. Do'stlar bilan keling, go'sht va qo'shimchalarni tanlang, keyin stolingizda grilda pishiring. Restoran Toshkent, Yunusobod, Chingiz Aytmatov 44 manzilida joylashgan."}}, {'slug': 'house-sauce', 'image': 'assets/images/restaurant-dish.png', 'date': '2026-06-17', 'status': 'published', 'title': {'en': 'House Sauce', 'jp': '特製だれ', 'ru': 'Фирменный соус', 'uz': 'Maxsus sous'}, 'summary': {'en': 'Sweet, smoky, and bright sauce made for grilled lamb.', 'jp': 'ラムに合う、甘みと香ばしさのある味。', 'ru': 'Сладкий, дымный и яркий соус для баранины на гриле.', 'uz': "Grilda pishgan qo'y go'shti uchun shirin, tutunli va yorqin sous."}, 'content': {'en': "The sauce finishes the bite. It balances lamb's richness with sweetness, smoke, and freshness. Dip the grilled meat while hot and try it with vegetables too.", 'jp': '焼きたての一口を仕上げるのが特製だれです。ラムの旨みを、甘み、香ばしさ、爽やかさで引き立てます。熱いうちに肉をつけ、野菜とも一緒にお楽しみください。', 'ru': 'Соус завершает вкус. Он уравновешивает насыщенность баранины сладостью, дымом и свежестью. Макайте горячее мясо и попробуйте его с овощами.', 'uz': "Maxsus sous har bir luqmani yakunlaydi. U qo'y go'shtining boy ta'mini shirinlik, tutun va yangilik bilan muvozanatlaydi. Issiq go'shtni sousga botiring, sabzavotlar bilan ham tatib ko'ring."}}]
INITIAL_BOOKINGS = [{'customer_name': 'Javo', 'phone': '9066744774', 'booking_date': '2026-06-17', 'booking_time': '19:00', 'people_count': 12, 'locale': 'en', 'status': 'new'}, {'customer_name': 'Javo', 'phone': '9066744774', 'booking_date': '2026-06-19', 'booking_time': '19:00', 'people_count': 4, 'locale': 'en', 'status': 'new'}, {'customer_name': 'Javo', 'phone': '9066744774', 'booking_date': '2026-06-17', 'booking_time': '19:00', 'people_count': 12, 'locale': 'en', 'status': 'accepted'}]


def seed(apps, schema_editor):
    BlogPost = apps.get_model("core", "BlogPost")
    Booking = apps.get_model("core", "Booking")
    for item in INITIAL_POSTS:
        BlogPost.objects.get_or_create(
            slug=item["slug"],
            defaults={
                "image": item["image"],
                "date": date.fromisoformat(item["date"]),
                "status": item["status"],
                "title_en": item["title"]["en"],
                "title_jp": item["title"]["jp"],
                "title_ru": item["title"]["ru"],
                "title_uz": item["title"]["uz"],
                "summary_en": item["summary"]["en"],
                "summary_jp": item["summary"]["jp"],
                "summary_ru": item["summary"]["ru"],
                "summary_uz": item["summary"]["uz"],
                "content_en": item["content"]["en"],
                "content_jp": item["content"]["jp"],
                "content_ru": item["content"]["ru"],
                "content_uz": item["content"]["uz"],
            },
        )
    for item in INITIAL_BOOKINGS:
        Booking.objects.get_or_create(
            customer_name=item["customer_name"],
            phone=item["phone"],
            booking_date=date.fromisoformat(item["booking_date"]),
            booking_time=time.fromisoformat(item["booking_time"]),
            people_count=item["people_count"],
            locale=item["locale"],
            status=item["status"],
        )


class Migration(migrations.Migration):
    dependencies = [("core", "0001_initial")]
    operations = [migrations.RunPython(seed, migrations.RunPython.noop)]
