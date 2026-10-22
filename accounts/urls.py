from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views

urlpatterns = [
    path('register', views.RegisterView.as_view(), name='register',),
    path('register_done', views.RegisterDoneView.as_view(), name='register_done',),
    path('login', views.AccountLoginView.as_view(), name='login',),
    path('logout', LogoutView.as_view(next_page='homepage'), name='logout',),
    path('withdraw', views.AccountDeletionView.as_view(), name='account_delete',),
    path('withdraw_done', views.AccountDeletionDoneView.as_view(), name='account_delete_done',),
]