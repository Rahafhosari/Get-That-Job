from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('in',views.home_in),
    path('register', views.registration),
    path('register-page', views.registration_page),
    path('log_in',views.log_in),
    path('log_out',views.log_out),
    path('profile',views.profile),
    path('edit',views.edit),
    path('booking',views.booking),
    path('admin',views.admin),
    path('addpartner',views.add_partner),
]