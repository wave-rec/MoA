from django.urls import path
from . import views

urlpatterns = [
    path("", views.product_list),
    path("recommend/", views.product_recommend),
    path("favorites/", views.favorite_list),
    path("<int:product_id>/", views.product_detail),
    path("<int:product_id>/favorite/", views.toggle_favorite),
]
