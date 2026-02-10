from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User

class Category(models.Model):
    """
    Örn: Konut, Arsa, İşyeri
    """
    name = models.CharField(max_length=50) # Kategori Adı
    slug = models.SlugField(max_length=50, unique=True) # URL'de görünecek isim (konut, arsa)

    def __str__(self):
        return self.name

class Listing(models.Model):
    """
    Bütün ilanların ortak özelliklerini tutan ana tablo.
    """
    # İlişkiler
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING) # Kategori silinirse ilana dokunma
    seller = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Satıcı")
    
    # Temel Bilgiler
    title = models.CharField(max_length=200, verbose_name="İlan Başlığı")
    price = models.IntegerField(verbose_name="Fiyat")
    description = models.TextField(verbose_name="Açıklama", blank=True)
    
    # Konum Bilgileri (İl/İlçe/Mahalle ileride detaylandırılabilir)
    city = models.CharField(max_length=100, verbose_name="Şehir")
    district = models.CharField(max_length=100, verbose_name="İlçe")
    
    # Medya
    # Fotoğrafları 'photos/%Y/%m/%d/' klasörüne tarihli olarak kaydedecek.
    main_photo = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    
    # Sistem Bilgileri
    is_published = models.BooleanField(default=True, verbose_name="Yayında mı?")
    list_date = models.DateTimeField(default=now, blank=True, verbose_name="Eklenme Tarihi")

    def __str__(self):
        return self.title
    
    # ... (Üstteki kodlar aynen kalsın) ...

class HousingDetail(models.Model):
    """
    Sadece KONUT kategorisindeki ilanlar için detaylar
    """
    # Seçenekler (Dropdown listeleri)
    ROOM_CHOICES = [
        ('1+0', '1+0'), ('1+1', '1+1'), ('2+1', '2+1'), ('3+1', '3+1'),
        ('4+1', '4+1'), ('5+1', '5+1'), ('Villa', 'Villa'), ('Müstakil', 'Müstakil')
    ]
    KITCHEN_CHOICES = [('Kapalı', 'Kapalı'), ('Amerikan', 'Amerikan'), ('Açık', 'Açık')]
    HEATING_CHOICES = [('Yok', 'Yok'), ('Kombi', 'Kombi'), ('Merkezi', 'Merkezi'), ('Klima', 'Klima')]

    # İlişki: Her ilanın sadece BİR konut detayı olabilir.
    listing = models.OneToOneField(Listing, on_delete=models.CASCADE, primary_key=True)
    
    # Özellikler
    emlak_tipi = models.CharField(max_length=20, choices=[('Satılık', 'Satılık'), ('Kiralık', 'Kiralık')])
    m2_brut = models.IntegerField(verbose_name="Brüt m²")
    m2_net = models.IntegerField(verbose_name="Net m²")
    oda_sayisi = models.CharField(max_length=20, choices=ROOM_CHOICES, verbose_name="Oda Sayısı")
    bina_yasi = models.IntegerField(verbose_name="Bina Yaşı")
    bulundugu_kat = models.CharField(max_length=20, verbose_name="Bulunduğu Kat") # Bodrum, Zemin vs olabileceği için string
    kat_sayisi = models.IntegerField(verbose_name="Kat Sayısı")
    isitma = models.CharField(max_length=20, choices=HEATING_CHOICES, verbose_name="Isıtma")
    banyo_sayisi = models.IntegerField(verbose_name="Banyo Sayısı")
    mutfak = models.CharField(max_length=20, choices=KITCHEN_CHOICES, verbose_name="Mutfak Tipi")
    
    # Evet/Hayır seçenekleri (Boolean)
    balkon = models.BooleanField(default=False, verbose_name="Balkon Var mı?")
    asansor = models.BooleanField(default=False, verbose_name="Asansör Var mı?")
    otopark = models.BooleanField(default=False, verbose_name="Otopark Var mı?")
    esyali = models.BooleanField(default=False, verbose_name="Eşyalı mı?")
    site_icerisinde = models.BooleanField(default=False, verbose_name="Site İçerisinde mi?")
    
    site_adi = models.CharField(max_length=100, blank=True, verbose_name="Site Adı")
    aidat = models.IntegerField(default=0, verbose_name="Aidat (TL)")

    def __str__(self):
        return f"{self.listing.title} - Konut Detayı"

class LandDetail(models.Model):
    """
    Sadece ARSA kategorisindeki ilanlar için detaylar
    """
    listing = models.OneToOneField(Listing, on_delete=models.CASCADE, primary_key=True)
    
    emlak_tipi = models.CharField(max_length=20, choices=[('Satılık', 'Satılık'), ('Kiralık', 'Kiralık')])
    imar_durumu = models.CharField(max_length=50, verbose_name="İmar Durumu") # Örn: Konut İmarlı, Tarla
    m2 = models.IntegerField(verbose_name="Metrekare")
    m2_fiyat = models.IntegerField(verbose_name="m² Fiyatı")
    
    # Teknik Detaylar
    ada_no = models.CharField(max_length=50, blank=True, verbose_name="Ada No")
    parsel_no = models.CharField(max_length=50, blank=True, verbose_name="Parsel No")
    pafta_no = models.CharField(max_length=50, blank=True, verbose_name="Pafta No")
    kaks = models.CharField(max_length=20, blank=True, verbose_name="Kaks (Emsal)")
    gabari = models.CharField(max_length=20, blank=True, verbose_name="Gabari")

    def __str__(self):
        return f"{self.listing.title} - Arsa Detayı"

# DİKKAT: Burası en solda, satır başında olmalı!
class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) # Beğenen Kullanıcı
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE) # Beğenilen İlan
    date_added = models.DateTimeField(auto_now_add=True) # Ne zaman beğendi?

    def __str__(self):
        return f"{self.user.username} - {self.listing.title}"
    
class ListingPhoto(models.Model):
    listing = models.ForeignKey(Listing, default=None, on_delete=models.CASCADE) # Hangi ilana ait?
    image = models.ImageField(upload_to='photos/%Y/%m/%d/') # Fotoğrafın kendisi
    
    def __str__(self):
        return self.listing.title