from django.contrib import admin
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
    model = ListingPhoto
    extra = 1 
    verbose_name = "Galeri Fotoğrafları"

# --- KATEGORİ GÖRÜNÜMÜNÜ DÜZELTEN YENİ KISIM ---
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # Bu satır sayesinde listede o "Konut > Satılık > Daire" yolunu göreceksin
    list_display = ('__str__', 'slug') 
    search_fields = ('name',)

# --- MEVCUT ADMİN AYARLARIN ---
class ListingAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'price', 'is_published')
    list_display_links = ('id', 'title')
    list_filter = ('category',)
    search_fields = ('title',)
    
    # Hem Konut, Hem Arsa, Hem de FOTOĞRAFLAR artık ilanın içinde görünecek.
    inlines = [HousingDetailInline, LandDetailInline, ListingPhotoInline]

# Category kaydını yukarıda @admin.register ile yaptığımız için burada sadece Listing kaldı
admin.site.register(Listing, ListingAdmin)