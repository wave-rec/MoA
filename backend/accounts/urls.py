from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup),
    path('login/', views.login),
    path('me/', views.me),
    path('logout/', views.logout),
    path('withdraw/', views.withdraw),
    path('favorites/', views.my_favorites),
    path('password/', views.change_password),
]
