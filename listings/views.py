from django.shortcuts import render, get_object_or_404, redirect
from .models import Listing, Category, Favorite, ListingPhoto
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ListingForm, HousingDetailForm, LandDetailForm
from django.core.paginator import Paginator
from django.http import JsonResponse

def index(request):
    # Son eklenen 3 ilanı getir (Vitrin için)
    listings = Listing.objects.order_by('-list_date').filter(is_published=True)[:3]

    context = {
        'listings': listings
    }
    return render(request, 'listings/index.html', context)

def listing_detail(request, listing_id):
    # 1. Ana İlanı Getir
    listing = get_object_or_404(Listing, pk=listing_id)

    # 2. GALERİ FOTOĞRAFLARINI GETİR (YENİ KISIM)
    # Veritabanına diyoruz ki: "ListingPhoto tablosuna git, bu ilana (listing) ait olanları bul."
    gallery_photos = ListingPhoto.objects.filter(listing=listing)

    # 3. Favori Kontrolü (Senin mevcut kodun)
    is_fav = False
    if request.user.is_authenticated:
        if Favorite.objects.filter(user=request.user, listing_id=listing.id).exists():
            is_fav = True

    context = {
        'listing': listing,
        'is_fav': is_fav,
        'gallery_photos': gallery_photos # <-- HTML'e gönderiyoruz
    }
    return render(request, 'listings/listing.html', context)
# Create your views here.

from django.shortcuts import render, get_object_or_404
from .models import Listing, Category  # Category'i import etmeyi unutma!

def listings(request):
    # 1. Tüm ilanları getir
    listings = Listing.objects.order_by('-list_date').filter(is_published=True)

    # 2. Sayfalayıcıyı Kur (Her sayfada 6 ilan olsun)
    paginator = Paginator(listings, 6)

    # 3. URL'den sayfa numarasını al (?page=2 gibi)
    page = request.GET.get('page')

    # 4. O sayfanın ilanlarını seç
    paged_listings = paginator.get_page(page)

    context = {
        # Artık 'listings' yerine 'paged_listings' gönderiyoruz
        'listings': paged_listings 
    }
    return render(request, 'listings/listings.html', context)

@login_required(login_url='login')
def create_listing(request):
    # Ana kategorileri (Konut, Arsa, İş Yeri vb.) en başta çekiyoruz
    main_categories = Category.objects.filter(parent=None)

    if request.method == 'POST':
        listing_form = ListingForm(request.POST, request.FILES)
        housing_form = HousingDetailForm(request.POST, prefix='konut')
        land_form = LandDetailForm(request.POST, prefix='arsa')

        if listing_form.is_valid():
            listing = listing_form.save(commit=False)
            listing.seller = request.user
            listing.save()

            # --- YENİ MANTIK: ANA KATEGORİYİ BULMA ---
            # Seçilen alt kategorinin (örn: Daire) en üstteki ana babasını buluyoruz
            current_cat = listing.category
            top_parent = current_cat
            while top_parent.parent is not None:
                top_parent = top_parent.parent
            
            ana_kategori_adi = top_parent.name # "Konut", "Arsa" vb.

            # KONUT VE ALT DALLARI İSE
            if ana_kategori_adi == 'Konut':
                if housing_form.is_valid():
                    housing = housing_form.save(commit=False)
                    housing.listing = listing
                    housing.save()
                    messages.success(request, 'Konut ilanı başarıyla oluşturuldu!')
                    return redirect('index')
                else:
                    listing.delete()
                    messages.error(request, 'Konut detaylarında hata var.')
            
            # ARSA VE ALT DALLARI İSE
            elif ana_kategori_adi == 'Arsa':
                if land_form.is_valid():
                    land = land_form.save(commit=False)
                    land.listing = listing
                    land.save()
                    messages.success(request, 'Arsa ilanı başarıyla oluşturuldu!')
                    return redirect('index')
                else:
                    listing.delete()
                    messages.error(request, 'Arsa detaylarında hata var.')
            
            else:
                # Şimdilik sadece Konut ve Arsa detay formları hazır olduğu için
                messages.success(request, f'{ana_kategori_adi} ilanı başarıyla oluşturuldu! (Detay formu henüz yok)')
                return redirect('index')

        else:
            messages.error(request, 'Lütfen ana bilgileri kontrol edin.')

    else:
        listing_form = ListingForm()
        housing_form = HousingDetailForm(prefix='konut')
        land_form = LandDetailForm(prefix='arsa')

    context = {
        'listing_form': listing_form,
        'housing_form': housing_form,
        'land_form': land_form,
        'main_categories': main_categories, # HTML'deki ilk kutu için
    }
    return render(request, 'listings/create.html', context)

@login_required(login_url='login')
def edit_listing(request, listing_id):
    # 1. İlanı Getir
    listing = get_object_or_404(Listing, id=listing_id)

    # 2. Güvenlik Kontrolü: İlanı düzenleyen kişi sahibi mi?
    if listing.seller != request.user:
        messages.error(request, 'Bu ilanı düzenleme yetkiniz yok!')
        return redirect('dashboard')

    # 3. İlanın Detayını Bul (Konut mu Arsa mı?)
    housing_detail = None
    land_detail = None
    
    # 'hasattr' ile ilişkili detay var mı kontrol ediyoruz
    if hasattr(listing, 'housingdetail'):
        housing_detail = listing.housingdetail
    elif hasattr(listing, 'landdetail'):
        land_detail = listing.landdetail

    # 4. POST İsteği (Form Kaydedildiğinde)
    if request.method == 'POST':
        # instance=listing diyerek 'güncelleme' modunda açıyoruz
        listing_form = ListingForm(request.POST, request.FILES, instance=listing)
        
        # Kategoriye göre ilgili formu doldur
        housing_form = HousingDetailForm(request.POST, instance=housing_detail) if housing_detail else None
        land_form = LandDetailForm(request.POST, instance=land_detail) if land_detail else None

        if listing_form.is_valid():
            listing_form.save()

            if housing_detail and housing_form.is_valid():
                housing_form.save()
            elif land_detail and land_form.is_valid():
                land_form.save()

            messages.success(request, 'İlan başarıyla güncellendi.')
            return redirect('dashboard')

    # 5. GET İsteği (Sayfa İlk Açıldığında)
    else:
        listing_form = ListingForm(instance=listing)
        housing_form = HousingDetailForm(instance=housing_detail) if housing_detail else None
        land_form = LandDetailForm(instance=land_detail) if land_detail else None

    context = {
        'listing': listing,
        'listing_form': listing_form,
        'housing_form': housing_form,
        'land_form': land_form,
        # Şablonda hangi formu göstereceğimizi anlamak için:
        'is_housing': housing_detail is not None,
        'is_land': land_detail is not None
    }

    return render(request, 'listings/edit.html', context)

def search(request):
    # 1. Tüm ilanları hazırlayalım
    queryset_list = Listing.objects.order_by('-list_date').filter(is_published=True)

    # 2. Kelime Araması (Keywords)
    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        if keywords:
            # Açıklamada (description) VEYA Başlıkta (title) arayalım
            queryset_list = queryset_list.filter(description__icontains=keywords) | queryset_list.filter(title__icontains=keywords)

    # 3. Şehir Araması (City)
    if 'city' in request.GET:
        city = request.GET['city']
        if city:
            # Şehir isminde tam eşleşme yerine "içeren" (icontains) yapalım ki 'Istanbul' yazsa da bulsun
            queryset_list = queryset_list.filter(city__icontains=city)

    context = {
        'listings': queryset_list,
        # Formdaki veriler silinmesin diye geri gönderiyoruz (values)
        'values': request.GET
    }
    return render(request, 'listings/search.html', context)

def category_listings(request, category_slug):
    # 1. Kategoriyi bul
    category = get_object_or_404(Category, slug=category_slug)

    # 2. O kategoriye ait ilanları getir
    listings = Listing.objects.filter(category=category, is_published=True).order_by('-list_date')

    # 3. Sayfalayıcıyı Kur (Burada da 6 ilan olsun)
    paginator = Paginator(listings, 6)

    # 4. Sayfa numarasını al
    page = request.GET.get('page')

    # 5. İlgili sayfayı seç
    paged_listings = paginator.get_page(page)

    context = {
        'listings': paged_listings, # Artık sayfalanmış listeyi gönderiyoruz
        'category': category
    }
    
    # Aynı şablonu kullandığımız için HTML tarafında ekstra bir şey yapmana gerek yok!
    return render(request, 'listings/listings.html', context)

@login_required(login_url='login')
def toggle_favorite(request, listing_id):
    # İlanı bul
    listing = get_object_or_404(Listing, id=listing_id)
    
    # Kullanıcı bu ilanı daha önce favorilemiş mi?
    favorite = Favorite.objects.filter(user=request.user, listing=listing)
    
    if favorite.exists():
        # Zaten varsa sil (Favoriden çıkar)
        favorite.delete()
        messages.success(request, 'İlan favorilerden çıkarıldı.')
    else:
        # Yoksa ekle
        Favorite.objects.create(user=request.user, listing=listing)
        messages.success(request, 'İlan favorilere eklendi ❤️')
    
    # İşlem bitince ilan detay sayfasına geri dön
    return redirect('listing_detail', listing_id=listing_id)

# --- API İÇİN GEREKLİ IMPORTLAR (GÜNCELLENDİ) ---
from rest_framework import generics
from rest_framework import filters # Arama için
from django_filters.rest_framework import DjangoFilterBackend # Filtreleme için
from .serializers import ListingSerializer

# Fonksiyon yerine Sınıf (Class) kullanıyoruz. Bu çok daha yetenekli.
class ListingListAPIView(generics.ListAPIView):
    # 1. Hangi verileri getireyim?
    queryset = Listing.objects.filter(is_published=True).order_by('-list_date')
    
    # 2. Hangi çevirmeni kullanayım?
    serializer_class = ListingSerializer
    
    # 3. Hangi filtreleri aktif edeyim?
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    # 4. Hangi alanlara göre filtreleme yapılsın?
    filterset_fields = ['city', 'district', 'price', 'category__slug'] # ?city=Ankara&price=5000
    
    # 5. Arama hangi alanlarda yapılsın?
    search_fields = ['title', 'description', 'city'] # ?search=deniz
    
    # 6. Sıralama izinleri
    ordering_fields = ['price', 'list_date'] # ?ordering=price
from django.shortcuts import render
from .models import Listing
import json

def map_view(request):
    listings = Listing.objects.exclude(lat__isnull=True).exclude(lon__isnull=True)
    
    locations = []
    for listing in listings:
        image_urls = []
        
        # 1. Ana Fotoğraf
        if listing.main_photo:
            image_urls.append(listing.main_photo.url)
        
        # 2. Galeri Fotoğrafları (related_name='photos' kullandığın için böyle çağırıyoruz)
        for photo in listing.photos.all(): 
            image_urls.append(photo.image.url)
            
        # 3. Detay Bilgisini Çek (related_name='housing_details' üzerinden)
        # Eğer modelde related_name vermediysen 'housing_details' yerine 'housingdetail' yazmalısın
        try:
            detail = listing.housing_details 
        except:
            detail = None

        # 4. Listeye Ekle
        locations.append({
            'id': listing.id,
            'title': listing.title,
            'price': float(listing.price),
            'lat': float(listing.lat),
            'lon': float(listing.lon),
            'images': image_urls,
            'url': f"/ilan/{listing.id}",
            'district': listing.district,
            'city': listing.city if hasattr(listing, 'city') else "Isparta",
            # Modalda (Hızlı Bakış) görünecek veriler
            'm2': detail.m2_brut if detail else "---",
            'rooms': detail.oda_sayisi if detail else "---",
            'floor': detail.bulundugu_kat if detail else "---",
            'heating': detail.isitma if detail else "---",
            'description': listing.description[:150] if listing.description else "Açıklama belirtilmemiş."
        })
    
    context = {
        'locations_json': json.dumps(locations) 
    }
    return render(request, 'listings/map.html', context)

def load_subcategories(request):
    parent_id = request.GET.get('parent_id')
    subcategories = Category.objects.filter(parent_id=parent_id).order_by('name')
    
    # Alt kategorileri JSON formatında (liste olarak) döndürüyoruz
    data = [
        {'id': sub.id, 'name': sub.name} for sub in subcategories
    ]
    return JsonResponse(data, safe=False)