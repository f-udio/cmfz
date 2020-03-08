from django.urls import path
from main import views

app_name = 'main'
urlpatterns = [
    path('index/', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('getcode/', views.get_code, name='getcode'),
    path('check_user/', views.check_user, name='check_user'),
]
