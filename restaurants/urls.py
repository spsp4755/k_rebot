from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RestaurantViewSet, saved_restaurants, recommend_restaurants, save_restaurant, unsave_restaurant

router = DefaultRouter()
router.register(r'restaurants', RestaurantViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('saved/', saved_restaurants, name='saved_restaurants'),
    path('recommendations/', recommend_restaurants, name='recommendations'),
    path('save/', save_restaurant, name='save_restaurant'),
    path('unsave/', unsave_restaurant, name='unsave_restaurant'),
]
