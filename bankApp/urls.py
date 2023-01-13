from django.urls import path, include
from . import views 
from django.contrib.auth import views as auth_view
from .decorators import already_loggedin

urlpatterns = [
    path('', views.home, name='home'),
    path('home', views.home, name='home'),
    path('sign-up', views.sign_up, name="sign_up"),
    # path('login/', (auth_view.LoginView.as_view(template_name='registration/login.html')), name='login'),
    path('login/', views.login, name='login'),
    path('login', views.login, name='login'),
    path('create-account', views.create_bank_account, name="create_bank_account"),
    path('transfer', views.make_transaction, name="make_transaction"),
]
