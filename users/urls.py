from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('giris', views.login_user, name='login'),
    path('kayit', views.register_user, name='register'),
    path('cikis', views.logout_user, name='logout'),
    path('ilanlarim', views.dashboard, name='dashboard'),
    path('ilan-sil/<int:listing_id>', views.delete_listing, name='delete_listing'),
    path('profil', views.profile_settings, name='profile_settings'),
    # Şifre Değiştirme Sayfası
    path('sifre-degistir/', auth_views.PasswordChangeView.as_view(template_name='users/password_change.html'), name='password_change'),
    # Şifre Değişince Gidilecek Başarı Sayfası
    path('sifre-degistir/basarili/', auth_views.PasswordChangeDoneView.as_view(template_name='users/password_success.html'), name='password_change_done'),
]