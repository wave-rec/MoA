from django.urls import path
from . import views

urlpatterns = [
    path("", views.product_list),
    path("recommend/", views.product_recommend),
    path("favorites/", views.favorite_list),
    path("banks/", views.bank_list),
    path("subscriptions/", views.subscription_list),
    path("<int:product_id>/", views.product_detail),
    path("<int:product_id>/favorite/", views.toggle_favorite),
    path("<int:product_id>/subscribe/", views.subscribe_product),
    path("<int:product_id>/ai-analysis/", views.get_ai_analysis),
]
