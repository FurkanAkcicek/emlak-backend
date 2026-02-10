from .models import Category

def menu_categories(request):
    # Veritabanındaki tüm kategorileri çekip her sayfaya 'global_categories' adıyla yollar
    categories = Category.objects.all()
    return {'global_categories': categories}