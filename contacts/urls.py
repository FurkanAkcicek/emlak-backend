from django.urls import path
from . import views

urlpatterns = [
    path('iletisim', views.contact, name='contact')
]