from django import forms
from .models import Listing, HousingDetail, LandDetail

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        # Kullanıcıdan istemeyeceğimiz alanları hariç tutuyoruz (tarih, satıcı, yayında mı vb.)
        exclude = ('seller', 'list_date', 'is_published')
        
        widgets = {
            'category': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Örn: Deniz Manzaralı 3+1'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'district': forms.TextInput(attrs={'class': 'form-control'}),
            'main_photo': forms.FileInput(attrs={'class': 'form-control'}),
        }

class HousingDetailForm(forms.ModelForm):
    class Meta:
        model = HousingDetail
        exclude = ('listing',) # Listing bağlantısını kodda yapacağız
        widgets = {
            'emlak_tipi': forms.Select(attrs={'class': 'form-select'}),
            'm2_brut': forms.NumberInput(attrs={'class': 'form-control'}),
            'm2_net': forms.NumberInput(attrs={'class': 'form-control'}),
            'oda_sayisi': forms.Select(attrs={'class': 'form-select'}),
            'bina_yasi': forms.NumberInput(attrs={'class': 'form-control'}),
            'bulundugu_kat': forms.TextInput(attrs={'class': 'form-control'}),
            'kat_sayisi': forms.NumberInput(attrs={'class': 'form-control'}),
            'isitma': forms.Select(attrs={'class': 'form-select'}),
            'banyo_sayisi': forms.NumberInput(attrs={'class': 'form-control'}),
            'mutfak': forms.Select(attrs={'class': 'form-select'}),
            'site_adi': forms.TextInput(attrs={'class': 'form-control'}),
            'aidat': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class LandDetailForm(forms.ModelForm):
    class Meta:
        model = LandDetail
        exclude = ('listing',)
        widgets = {
            'emlak_tipi': forms.Select(attrs={'class': 'form-select'}),
            'imar_durumu': forms.TextInput(attrs={'class': 'form-control'}),
            'm2': forms.NumberInput(attrs={'class': 'form-control'}),
            'm2_fiyat': forms.NumberInput(attrs={'class': 'form-control'}),
            'ada_no': forms.TextInput(attrs={'class': 'form-control'}),
            'parsel_no': forms.TextInput(attrs={'class': 'form-control'}),
            'pafta_no': forms.TextInput(attrs={'class': 'form-control'}),
            'kaks': forms.TextInput(attrs={'class': 'form-control'}),
            'gabari': forms.TextInput(attrs={'class': 'form-control'}),
        }