from django.core.management.base import BaseCommand
from locations.models import Country, Region

class Command(BaseCommand):
    help = 'Заполняет БД странами и регионами (Украина и Польша) на трех языках'

    def handle(self, *args, **options):
        ua, created = Country.objects.get_or_create(
            code='UA',
            defaults={
                'name_ru': 'Украина',
                'name_uk': 'Україна',
                'name_en': 'Ukraine',
            }
        )

        ua_regions = [
            {"uk": "Вінницька область", "ru": "Винницкая область", "en": "Vinnytsia Oblast"},
            {"uk": "Волинська область", "ru": "Волынская область", "en": "Volyn Oblast"},
            {"uk": "Дніпропетровська область", "ru": "Днепропетровская область", "en": "Dnipropetrovsk Oblast"},
            {"uk": "Донецька область", "ru": "Донецкая область", "en": "Donetsk Oblast"},
            {"uk": "Житомирська область", "ru": "Житомирская область", "en": "Zhytomyr Oblast"},
            {"uk": "Закарпатська область", "ru": "Закарпатская область", "en": "Zakarpattia Oblast"},
            {"uk": "Запорізька область", "ru": "Запорожская область", "en": "Zaporizhzhia Oblast"},
            {"uk": "Івано-Франківська область", "ru": "Ивано-Франковская область", "en": "Ivano-Frankivsk Oblast"},
            {"uk": "Київська область", "ru": "Киевская область", "en": "Kyiv Oblast"},
            {"uk": "Кіровоградська область", "ru": "Кировоградская область", "en": "Kirovohrad Oblast"},
            {"uk": "Луганська область", "ru": "Луганская область", "en": "Luhansk Oblast"},
            {"uk": "Львівська область", "ru": "Львовская область", "en": "Lviv Oblast"},
            {"uk": "Миколаївська область", "ru": "Николаевская область", "en": "Mykolaiv Oblast"},
            {"uk": "Одеська область", "ru": "Одесская область", "en": "Odesa Oblast"},
            {"uk": "Полтавська область", "ru": "Полтавская область", "en": "Poltava Oblast"},
            {"uk": "Рівненська область", "ru": "Ровенская область", "en": "Rivne Oblast"},
            {"uk": "Сумська область", "ru": "Сумская область", "en": "Sumy Oblast"},
            {"uk": "Тернопільська область", "ru": "Тернопольская область", "en": "Ternopil Oblast"},
            {"uk": "Харківська область", "ru": "Харьковская область", "en": "Kharkiv Oblast"},
            {"uk": "Херсонська область", "ru": "Херсонская область", "en": "Kherson Oblast"},
            {"uk": "Хмельницька область", "ru": "Хмельницкая область", "en": "Khmelnytskyi Oblast"},
            {"uk": "Черкаська область", "ru": "Черкасская область", "en": "Cherkasy Oblast"},
            {"uk": "Чернівецька область", "ru": "Черновицкая область", "en": "Chernivtsi Oblast"},
            {"uk": "Чернігівська область", "ru": "Черниговская область", "en": "Chernihiv Oblast"},
            {"uk": "АР Крим", "ru": "АР Крым", "en": "Autonomous Republic of Crimea"},
            {"uk": "Київ", "ru": "Киев", "en": "Kyiv"},
            {"uk": "Севастополь", "ru": "Севастополь", "en": "Sevastopol"},
        ]

        pl, created = Country.objects.get_or_create(
            code='PL',
            defaults={
                'name_ru': 'Польша',
                'name_uk': 'Польща',
                'name_en': 'Poland',
            }
        )

        pl_regions = [
            {"uk": "Нижньосілезьке", "ru": "Нижнесилезское", "en": "Lower Silesian"},
            {"uk": "Куявсько-Поморське", "ru": "Куявско-Поморское", "en": "Kuyavian-Pomeranian"},
            {"uk": "Люблінське", "ru": "Люблинское", "en": "Lublin"},
            {"uk": "Любуське", "ru": "Любушское", "en": "Lubusz"},
            {"uk": "Лодзинське", "ru": "Лодзинское", "en": "Lodz"},
            {"uk": "Малопольське", "ru": "Малопольское", "en": "Lesser Poland"},
            {"uk": "Мазовецьке", "ru": "Мазовецкое", "en": "Mazovian"},
            {"uk": "Опольське", "ru": "Опольское", "en": "Opole"},
            {"uk": "Підкарпатське", "ru": "Подкарпатское", "en": "Subcarpathian"},
            {"uk": "Підляське", "ru": "Подляское", "en": "Podlaskie"},
            {"uk": "Поморське", "ru": "Поморское", "en": "Pomeranian"},
            {"uk": "Сілезьке", "ru": "Силезское", "en": "Silesian"},
            {"uk": "Свентокшиське", "ru": "Свентокшиское", "en": "Holy Cross"},
            {"uk": "Вармінсько-Мазурське", "ru": "Варминско-Мазурское", "en": "Warmian-Masurian"},
            {"uk": "Великопольське", "ru": "Великопольское", "en": "Greater Poland"},
            {"uk": "Західнопоморське", "ru": "Западнопоморское", "en": "West Pomeranian"},
        ]

        def create_regions(country, data):
            for item in data:
                Region.objects.get_or_create(
                    country=country,
                    name_uk=item['uk'],
                    defaults={
                        'name_ru': item['ru'],
                        'name_en': item['en'],
                    }
                )

        create_regions(ua, ua_regions)
        create_regions(pl, pl_regions)

        self.stdout.write(self.style.SUCCESS('Данные успешно загружены (UA, PL)'))