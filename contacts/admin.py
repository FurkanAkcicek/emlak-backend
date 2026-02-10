from django.contrib import admin
from .models import Contact

class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'listing', 'email', 'contact_date') # Listede neler görünsün
    list_display_links = ('id', 'name') # Hangisine tıklayınca detay açılsın
    search_fields = ('name', 'email', 'listing') # Arama kutusu neye baksın
    list_per_page = 25 # Sayfada kaç mesaj olsun

admin.site.register(Contact, ContactAdmin)