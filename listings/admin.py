from django.contrib import admin
# 1. BURAYA ListingPhoto'yu ekledik
from .models import Category, Listing, HousingDetail, LandDetail, ListingPhoto 

# --- MEVCUT KODLARIN (AYNEN KALIYOR) ---
class HousingDetailInline(admin.StackedInline):
    model = HousingDetail
    extra = 0
    verbose_name = "Konut Detayları (Sadece Konut ise doldurun)"

class LandDetailInline(admin.StackedInline):
    model = LandDetail
    extra = 0
    verbose_name = "Arsa Detayları (Sadece Arsa ise doldurun)"

# --- 2. YENİ EKLENEN KISIM: GALERİ FOTOĞRAFLARI ---
class ListingPhotoInline(admin.TabularInline): 
    # Not: 'TabularInline' kullandım, fotoğraflar alt alta değil yan yana daha az yer kaplasın diye.
    model = ListingPhoto
    extra = 1 # Başlangıçta 1 tane boş resim yükleme kutusu göster
    verbose_name = "Galeri Fotoğrafları"

# --- MEVCUT ADMİN AYARLARIN ---
class ListingAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'price', 'is_published')
    list_display_links = ('id', 'title')
    list_filter = ('category',)
    search_fields = ('title',)
    
    # 3. BURAYI BİRLEŞTİRDİK:
    # Hem Konut, Hem Arsa, Hem de FOTOĞRAFLAR artık ilanın içinde görünecek.
    inlines = [HousingDetailInline, LandDetailInline, ListingPhotoInline]

admin.site.register(Category)
admin.site.register(Listing, ListingAdmin)