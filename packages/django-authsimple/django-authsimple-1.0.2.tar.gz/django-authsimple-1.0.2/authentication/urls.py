from django.urls import path, include
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('verify/<uuid:code>', views.verify, name='verify'),
    path('verify/new/', views.verify_new, name='verify_new'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('reset_password/<uuid:code>',
         views.reset_password, name='reset_password'),
]
