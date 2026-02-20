from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
from django.utils.text import slugify

class Category(models.Model):
    """
    Hiyerarşik Kategori Yapısı
    Örn: Konut -> Satılık Konut -> Daire
    """
    name = models.CharField(max_length=100, verbose_name="Kategori Adı")
    # Kendi kendine bağlanma (Self-referential)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategories', verbose_name="Üst Kategori")
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            # İsimden otomatik slug oluşturur (örn: "İş Yeri" -> "is-yeri")
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        # Admin panelinde tam yolu görmek için: Konut > Satılık > Daire
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return ' > '.join(full_path[::-1])

    class Meta:
        verbose_name_plural = "Categories"

class Listing(models.Model):
    """
    Bütün ilanların ortak özelliklerini tutan ana tablo.
    """
    # İlişkiler
    # category artik en alt seviyedeki kategoriyi tutacak (örn: Daire)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name="Kategori")
    seller = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Satıcı")
    
    # Temel Bilgiler
    title = models.CharField(max_length=200, verbose_name="İlan Başlığı")
    price = models.BigIntegerField(verbose_name="Fiyat") # Çok yüksek rakamlar için BigInteger daha güvenli
    description = models.TextField(verbose_name="Açıklama", blank=True)
    
    # Konum Bilgileri
    city = models.CharField(max_length=100, verbose_name="Şehir")
    district = models.CharField(max_length=100, verbose_name="İlçe")
    
    # Medya
    main_photo = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True, verbose_name="Ana Fotoğraf")
    
    # Sistem Bilgileri
    is_published = models.BooleanField(default=True, verbose_name="Yayında mı?")
    list_date = models.DateTimeField(default=now, blank=True, verbose_name="Eklenme Tarihi")
    
    # Konum (Harita koordinatları)
    lat = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, verbose_name="Enlem (Latitude)")
    lon = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, verbose_name="Boylam (Longitude)")

    def __str__(self):
        return self.title

from django.db import models

class HousingDetail(models.Model):
    # Ana İlan ile bağlantı
    listing = models.OneToOneField('Listing', on_delete=models.CASCADE, primary_key=True, related_name='housing_details')

    # --- SEÇENEK LİSTELERİ (Choices) ---
    ROOM_CHOICES = [
        ('1+0', '1+0 (Stüdyo)'), ('1+1', '1+1'), ('2+0', '2+0'), ('2+1', '2+1'), 
        ('2+2', '2+2'), ('3+1', '3+1'), ('3+2', '3+2'), ('4+1', '4+1'), 
        ('4+2', '4+2'), ('5+1', '5+1'), ('5+2', '5+2'), ('6+1', '6+1'), 
        ('6+2', '6+2'), ('7+ ve üzeri', '7+ ve üzeri')
    ]

    FLOOR_CHOICES = [
        ('Bodrum Kat', 'Bodrum Kat'), ('Zemin Kat', 'Zemin Kat'), ('Bahçe Katı', 'Bahçe Katı'),
        ('Giriş Katı', 'Giriş Katı'), ('Yüksek Giriş', 'Yüksek Giriş'), ('Müstakil', 'Müstakil'),
        ('1', '1. Kat'), ('2', '2. Kat'), ('3', '3. Kat'), ('4', '4. Kat'), ('5', '5. Kat'),
        ('10-20 arası', '10-20. Kat arası'), ('20 ve üzeri', '20. Kat ve üzeri'), ('En Üst Kat', 'En Üst Kat')
    ]

    # --- 1. SEKMELİK: TEKNİK ÖZELLİKLER (Güncellenmiş Seçenekler) ---
    m2_brut = models.PositiveIntegerField(verbose_name="Brüt m²")
    m2_net = models.PositiveIntegerField(verbose_name="Net m²")
    
    # Burayı güncelledik: choices eklendi
    oda_sayisi = models.CharField(max_length=20, choices=ROOM_CHOICES, default='2+1', verbose_name="Oda Sayısı")
    
    bina_yasi = models.IntegerField(default=0, verbose_name="Bina Yaşı")
    
    # Burayı güncelledik: choices eklendi
    bulundugu_kat = models.CharField(max_length=50, choices=FLOOR_CHOICES, default='Giriş Katı', verbose_name="Bulunduğu Kat")
    
    kat_sayisi = models.IntegerField(verbose_name="Toplam Kat Sayısı")
    banyo_sayisi = models.PositiveIntegerField(default=1, verbose_name="Banyo Sayısı")
    aidat = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Aidat (TL)")
    
    # Diğer Seçenekli Alanlar (Aynen Kalıyor)
    ISITMA_CHOICES = [('Yok', 'Yok'), ('Kombi', 'Kombi'), ('Merkezi', 'Merkezi'), ('Klima', 'Klima'), ('Yerden Isıtma', 'Yerden Isıtma')]
    isitma = models.CharField(max_length=50, choices=ISITMA_CHOICES, default='Yok', verbose_name="Isıtma Tipi")
    
    ESYA_CHOICES = [('Eşyalı', 'Eşyalı'), ('Eşyasız', 'Eşyasız')]
    esya_durumu = models.CharField(max_length=20, choices=ESYA_CHOICES, default='Eşyasız', verbose_name="Eşya Durumu")
    
    KULLANIM_CHOICES = [('Boş', 'Boş'), ('Kiracılı', 'Kiracılı'), ('Mülk Sahibi', 'Mülk Sahibi')]
    kullanim_durumu = models.CharField(max_length=50, choices=KULLANIM_CHOICES, blank=True, verbose_name="Kullanım Durumu")

    OTOPARK_CHOICES = [('Yok', 'Yok'), ('Açık Otopark', 'Açık Otopark'), ('Kapalı Otopark', 'Kapalı Otopark'), ('Açık & Kapalı', 'Açık & Kapalı')]
    otopark = models.CharField(max_length=50, choices=OTOPARK_CHOICES, default='Yok', verbose_name="Otopark")

    MUTFAK_CHOICES = [('Kapalı Mutfak', 'Kapalı Mutfak'), ('Amerikan Mutfak', 'Amerikan Mutfak'), ('Açık Mutfak', 'Açık Mutfak')]
    mutfak_tipi = models.CharField(max_length=50, choices=MUTFAK_CHOICES, blank=True, verbose_name="Mutfak Tipi")

    TAPU_CHOICES = [('Kat Mülkiyeti', 'Kat Mülkiyeti'), ('Kat İrtifakı', 'Kat İrtifakı'), ('Arsa Tapulu', 'Arsa Tapulu'), ('Hisseli Tapu', 'Hisseli Tapu')]
    tapu_durumu = models.CharField(max_length=50, choices=TAPU_CHOICES, blank=True, verbose_name="Tapu Durumu")

    # --- 2. VE 3. SEKMELER (Boolean alanların aynen kalabilir) ---
    site_icinde = models.BooleanField(default=False, verbose_name="Site İçerisinde")
    krediye_uygun = models.BooleanField(default=False, verbose_name="Krediye Uygun")
    takas = models.BooleanField(default=False, verbose_name="Takaslı")
    balkon = models.BooleanField(default=False, verbose_name="Balkon Var")
    asansor = models.BooleanField(default=False, verbose_name="Asansör Var")
    ebeveyn_banyosu = models.BooleanField(default=False)
    giyinme_odasi = models.BooleanField(default=False)
    camasir_odasi = models.BooleanField(default=False)
    kiler = models.BooleanField(default=False)
    teras = models.BooleanField(default=False)
    ankastre_mutfak = models.BooleanField(default=False)
    somine = models.BooleanField(default=False, verbose_name="Şömine")
    akilli_ev = models.BooleanField(default=False)
    celik_kapi = models.BooleanField(default=False)
    goruntulu_diafon = models.BooleanField(default=False)
    fiber_internet = models.BooleanField(default=False)

    yuzme_havuzu = models.BooleanField(default=False)
    cocuk_parki = models.BooleanField(default=False)
    spor_salonu = models.BooleanField(default=False)
    guvenlik = models.BooleanField(default=False)
    jenerator = models.BooleanField(default=False)
    deniz_manzarasi = models.BooleanField(default=False)
    dogamanzarasi = models.BooleanField(default=False)
    sehir_manzarasi = models.BooleanField(default=False)
    metroya_yakin = models.BooleanField(default=False)
    metrobuse_yakin = models.BooleanField(default=False)
    avmye_yakin = models.BooleanField(default=False)
    okula_yakin = models.BooleanField(default=False)
    hastaneye_yakin = models.BooleanField(default=False)

    def __str__(self):
        return f"Konut Detayı: {self.listing.title}"

class LandDetail(models.Model):
    """
    Sadece ARSA kategorisindeki ilanlar için detaylar
    """
    listing = models.OneToOneField(Listing, on_delete=models.CASCADE, primary_key=True)
    
    emlak_tipi = models.CharField(max_length=20, choices=[('Satılık', 'Satılık'), ('Kiralık', 'Kiralık')])
    imar_durumu = models.CharField(max_length=50, verbose_name="İmar Durumu")
    m2 = models.IntegerField(verbose_name="Metrekare")
    m2_fiyat = models.IntegerField(verbose_name="m² Fiyatı")
    
    ada_no = models.CharField(max_length=50, blank=True, verbose_name="Ada No")
    parsel_no = models.CharField(max_length=50, blank=True, verbose_name="Parsel No")
    pafta_no = models.CharField(max_length=50, blank=True, verbose_name="Pafta No")
    kaks = models.CharField(max_length=20, blank=True, verbose_name="Kaks (Emsal)")
    gabari = models.CharField(max_length=20, blank=True, verbose_name="Gabari")

    def __str__(self):
        return f"{self.listing.title} - Arsa Detayı"

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.listing.title}"
    
class ListingPhoto(models.Model):
    listing = models.ForeignKey(Listing, default=None, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='photos/%Y/%m/%d/')
    
    def __str__(self):
        return f"Photo for {self.listing.title}"