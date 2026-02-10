from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from listings.models import Listing
from contacts.models import Contact  # <-- YENİ: Mesajları çekmek için bunu ekledik
from listings.models import Favorite

def login_user(request):
    if request.method == 'POST':
        kullanici_adi = request.POST['username']
        sifre = request.POST['password']
        user = authenticate(request, username=kullanici_adi, password=sifre)

        if user is not None:
            login(request, user)
            messages.success(request, 'Başarıyla giriş yaptınız.')
            return redirect('index')
        else:
            messages.error(request, 'Kullanıcı adı veya şifre hatalı.')
            return redirect('login')
    
    return render(request, 'users/login.html')

def register_user(request):
    if request.method == 'POST':
        ad = request.POST['first_name']
        soyad = request.POST['last_name']
        kullanici_adi = request.POST['username']
        email = request.POST['email']
        sifre = request.POST['password']
        sifre2 = request.POST['password_confirm']

        if sifre != sifre2:
            messages.error(request, 'Şifreler uyuşmuyor!')
            return redirect('register')
        
        if User.objects.filter(username=kullanici_adi).exists():
            messages.error(request, 'Bu kullanıcı adı zaten alınmış.')
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Bu email zaten kayıtlı.')
            return redirect('register')

        user = User.objects.create_user(username=kullanici_adi, email=email, password=sifre)
        user.first_name = ad
        user.last_name = soyad
        user.save()

        messages.success(request, 'Kayıt başarılı! Şimdi giriş yapabilirsiniz.')
        return redirect('login')

    return render(request, 'users/register.html')

def logout_user(request):
    logout(request)
    messages.success(request, 'Çıkış yapıldı.')
    return redirect('index')

@login_required(login_url='login')
def dashboard(request):
    # 1. Kendi ilanlarını getir
    listings = Listing.objects.filter(seller=request.user).order_by('-list_date')

    # 2. Mesajları getir
    listing_ids = listings.values_list('id', flat=True) 
    contacts = Contact.objects.order_by('-contact_date').filter(listing_id__in=listing_ids)

    # 3. FAVORİLERİ GETİR (YENİ KISIM)
    # Kullanıcının favorilediği kayıtları alalım
    favorites = Favorite.objects.filter(user=request.user).order_by('-date_added')

    context = {
        'listings': listings,
        'contacts': contacts,
        'favorites': favorites # <-- HTML'e gönderiyoruz
    }
    return render(request, 'users/dashboard.html', context)

@login_required(login_url='login')
def delete_listing(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)

    if listing.seller != request.user:
        messages.error(request, 'Bu ilanı silme yetkiniz yok!')
        return redirect('dashboard')

    listing.delete()
    messages.success(request, 'İlan başarıyla silindi.')
    return redirect('dashboard')

@login_required(login_url='login')
def profile_settings(request):
    if request.method == 'POST':
        # Formdan gelen verileri al
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        
        # Kullanıcının mevcut bilgilerini güncelle
        user = request.user
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        
        # E-posta kontrolü (Başkasının mailini almasın)
        if User.objects.exclude(pk=user.pk).filter(email=email).exists():
            messages.error(request, 'Bu e-posta adresi başka bir kullanıcı tarafından kullanılıyor.')
            return redirect('profile_settings')

        user.save()
        messages.success(request, 'Profil bilgileriniz başarıyla güncellendi.')
        return redirect('profile_settings')

    return render(request, 'users/profile.html')