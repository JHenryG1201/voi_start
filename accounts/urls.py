from django.urls import path
from . import views

urlpatterns = [
    path('register', views.RegisterView.as_view(), name='register',),
    path('register_scuccess', views.RegisterSuccessView.as_view(), name='register_success',),
]