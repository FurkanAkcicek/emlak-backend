from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Contact

def contact(request):
    if request.method == 'POST':
        # Formdan gelen verileri al
        listing_id = request.POST['listing_id']
        listing = request.POST['listing']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        user_id = request.POST['user_id']
        realtor_email = request.POST['realtor_email'] # Emlakçının maili (ilerde mail atarsak diye)

        # SPAM KONTROLÜ: Eğer kullanıcı giriş yapmışsa, aynı ilana daha önce mesaj atmış mı?
        if request.user.is_authenticated:
            user_id = request.user.id
            has_contacted = Contact.objects.all().filter(listing_id=listing_id, user_id=user_id)
            if has_contacted:
                messages.error(request, 'Bu ilan için zaten bir talep oluşturdunuz. Size dönüş yapılacaktır.')
                return redirect('/ilan/'+listing_id)

        # Veritabanına Kaydet
        contact = Contact(listing=listing, listing_id=listing_id, name=name, email=email, phone=phone, message=message, user_id=user_id)
        contact.save()

        # Başarılı Mesajı Ver
        messages.success(request, 'Talebiniz alındı! Emlak danışmanımız en kısa sürede size dönüş yapacaktır.')
        
        # İlan detay sayfasına geri dön
        return redirect('/ilan/'+listing_id)