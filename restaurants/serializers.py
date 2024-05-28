from rest_framework import serializers
from .models import Restaurant, SavedRestaurant

class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = '__all__'

class SavedRestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedRestaurant
        fields = '__all__'
