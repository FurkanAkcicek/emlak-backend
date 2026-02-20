from django.core.management.base import BaseCommand
from listings.models import Category
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Emlak kategorilerini hatasız yükler'

    def handle(self, *args, **kwargs):
        # Senin devasa kategori listen
        data = {
            "Konut": {
                "Satılık Konut": ["Daire", "Rezidans", "Müstakil Ev", "Villa", "Yazlık", "Dubleks / Tripleks", "Bahçe Katı", "Çatı Dubleksi", "Prefabrik Ev", "Tiny House"],
                "Kiralık Konut": ["Rezidans", "Müstakil Ev", "Villa", "Yazlık", "Günlük Kiralık Daire", "Apart / Apart Daire", "Oda"],
                "Konut Projeleri": ["Satılık Projeler", "Devam Eden Projeler", "Kentsel Dönüşüm Projeleri"]
            },
            "Arsa": {
                "Satılık Arsa": ["Konut İmarlı", "Ticari İmarlı", "Sanayi İmarlı", "Tarla", "Bağ & Bahçe", "Zeytinlik", "Hobi Bahçesi", "Turizm İmarlı Arsa", "Villa Arsası", "Kat Karşılığı Arsa"],
                "Kiralık Arsa": ["Tarla", "Depolama Alanı", "Otopark Arsası"]
            },
            "İş Yeri": {
                "Satılık İş Yeri": ["Ofis", "Büro", "Plaza Katı", "Dükkan & Mağaza", "AVM Dükkanı", "Restoran & Kafe", "Otel", "Pansiyon", "Fabrika", "Atölye", "İmalathane", "Depo", "İş Hanı Katı"],
                "Kiralık İş Yeri": ["Ofis", "Coworking Alanı", "Dükkan", "Depo", "Atölye", "Restoran & Kafe"]
            },
            "Günlük Kiralık - Kısa Dönem": {
                "Genel": ["Günlük Daire", "Günlük Villa", "Günlük Bungalov", "Saatlik Ofis"]
            },
            "Bina": {
                "Satılık Bina": ["Apartman", "Komple Bina", "İş Merkezi", "Plaza", "AVM"],
                "Kiralık Bina": ["Komple Bina", "İş Merkezi Katı"]
            },
            "Turistik Tesis": {
                "Genel": ["Otel", "Butik Otel", "Tatil Köyü", "Apart Otel", "Pansiyon", "Kamp Alanı", "Bungalov Tesisi"]
            },
            "Devremülk": {
                "Genel": ["Satılık Devremülk", "Kiralık Devremülk"]
            }
        }

        for main_name, sub_cats in data.items():
            # Ana Kategori (Konut, Arsa vb.)
            main_slug = slugify(main_name)
            main_cat, _ = Category.objects.get_or_create(
                name=main_name, parent=None, defaults={'slug': main_slug}
            )

            for sub_name, items in sub_cats.items():
                if sub_name == "Genel":
                    parent_for_items = main_cat
                else:
                    # Alt Kategori (Satılık Konut, Kiralık Konut vb.)
                    sub_slug = slugify(f"{main_name}-{sub_name}")
                    parent_for_items, _ = Category.objects.get_or_create(
                        name=sub_name, parent=main_cat, defaults={'slug': sub_slug}
                    )
                
                for item_name in items:
                    # En alt birim (Daire, Rezidans vb.)
                    # Çakışma olmasın diye slug'ı: 'ebeveyn-adı + kendi-adı' yapıyoruz
                    unique_slug = slugify(f"{parent_for_items.name}-{item_name}")
                    Category.objects.get_or_create(
                        name=item_name, parent=parent_for_items, defaults={'slug': unique_slug}
                    )
        
        self.stdout.write(self.style.SUCCESS('Kategoriler mermi gibi dizildi! Başarılı.'))