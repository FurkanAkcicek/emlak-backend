from rest_framework import serializers
from .models import Listing, ListingPhoto, HousingDetail, LandDetail

# 1. Galeri Fotoğrafları İçin Serializer
class ListingPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListingPhoto
        fields = ('image',) # Sadece resim yolunu versin yeter

# 2. Konut Detayları İçin Serializer
class HousingDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = HousingDetail
        exclude = ('listing',) # 'listing' alanı zaten üstte var, tekrar etmesin

# 3. Arsa Detayları İçin Serializer
class LandDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = LandDetail
        exclude = ('listing',)

# 4. ANA İLAN SERIALIZER (Hepsini Birleştiren Patron)
class ListingSerializer(serializers.ModelSerializer):
    # İlişkili verileri buraya bağlıyoruz
    # 'listingphoto_set' -> Django'nun otomatik verdiği isim (Child Relation)
    # 'housingdetail' -> OneToOne olduğu için direkt isimle çağrılır
    
    gallery_photos = ListingPhotoSerializer(source='listingphoto_set', many=True, read_only=True)
    housing_detail = HousingDetailSerializer(source='housingdetail', read_only=True)
    land_detail = LandDetailSerializer(source='landdetail', read_only=True)

    class Meta:
        model = Listing
        # Artık standart alanların yanına, yukarıdaki özel alanları da ekliyoruz
        fields = (
            'id', 'title', 'price', 'city', 'district', 'list_date', 'is_published',
            'main_photo', 'description', # Ana fotoyu ve açıklamayı da ekleyelim
            'housing_detail', 'land_detail', 'gallery_photos'
        )