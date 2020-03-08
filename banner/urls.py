from django.urls import path
from banner import views

app_name = 'banner'

urlpatterns = [
    path('save/', views.save_banner, name='save'),
    path('show/', views.show_banner, name='show'),
    path('edit/', views.edit_banner, name='edit'),
]
