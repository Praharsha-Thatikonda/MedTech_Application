from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('doctors/', views.doctors, name='doctors'),
    path('hospitals/', views.hospitals, name='hospitals'),
    path('ailab/', views.ailab, name='ailab'),
    path('map/', views.map_view, name='map'),
    path('profile/', views.profile, name='profile'),
    path('api/chat', views.chat_api, name='chat_api'),
    path('transportation/', views.transportation, name='transportation'),
]
