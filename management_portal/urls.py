from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('search-result/', views.search_result, name='search_result'),
    path('user/', include('user_management.urls'), name='user'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('customers/', include('customers.urls'), name='customers'),
    path('heartbeat/', include('heartbeat.urls'), name='heartbeat'),
    path('licenses/', include('licenses.urls'), name='licenses'),
    path('updates/', include('updates.urls'), name='updates'),
]
