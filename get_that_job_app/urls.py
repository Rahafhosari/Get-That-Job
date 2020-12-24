from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('in',views.home_in),
    path('register', views.registration),
    path('register-page', views.registration_page),
    path('log_in',views.log_in),
    path('log_out',views.log_out),
    # path('profile',views.profile),
    # path('booking',views.booking),
    # path('partner',views.partner),
]