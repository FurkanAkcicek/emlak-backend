from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# Uygulama adı (Namespace sorunu yaşarsak bu bizi kurtarır)
#app_name = 'listings'

urlpatterns = [
    # Ana Sayfa
    path('', views.index, name='index'), 
    
    # İlan Listeleme
    path('ilanlar/', views.listings, name='listings'),
    
    # İlan Detayı
    path('ilan/<int:listing_id>', views.listing_detail, name='listing_detail'),
    
    # Arama
    path('arama', views.search, name='search'),

    path('harita/', views.map_view, name='map_view'),
    
    # İlan Verme (Sonundaki virgüle dikkat!)
    path('ilan-ver', views.create_listing, name='create_listing'),
    
    # İlan Düzenleme
    path('ilan-duzenle/<int:listing_id>', views.edit_listing, name='edit_listing'),

    path('kategori/<slug:category_slug>', views.category_listings, name='category_listings'),

    path('favori/<int:listing_id>', views.toggle_favorite, name='toggle_favorite'),

    path('api/ilanlar/', views.ListingListAPIView.as_view(), name='api_listings'),

    # --- JWT GİRİŞ KAPILARI ---
    # Kullanıcı adı/şifre gönderip TOKEN aldığımız yer (Login)
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    
    # Token süresi bitince yenisini aldığımız yer (Refresh)
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]