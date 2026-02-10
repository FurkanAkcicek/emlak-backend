from django.db import models
from datetime import datetime

class Contact(models.Model):
    listing = models.CharField(max_length=200) # İlanın Başlığı
    listing_id = models.IntegerField()         # İlanın ID numarası
    name = models.CharField(max_length=200)    # Mesajı Atan Kişi
    email = models.CharField(max_length=100)   # E-postası
    phone = models.CharField(max_length=100)   # Telefonu
    message = models.TextField(blank=True)     # Mesajı
    contact_date = models.DateTimeField(default=datetime.now, blank=True) # Tarih
    user_id = models.IntegerField(blank=True)  # Mesajı atan üye mi? (ID'si)

    def __str__(self):
        return self.name