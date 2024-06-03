from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Restaurant, SavedRestaurant
from .serializers import RestaurantSerializer, SavedRestaurantSerializer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from numpy import int64

class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [IsAuthenticated]

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def saved_restaurants(request):
    user = request.user
    saved_restaurants = SavedRestaurant.objects.filter(user=user)
    serializer = SavedRestaurantSerializer(saved_restaurants, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def recommend_restaurants(request):
    user = request.user
    saved_restaurants = SavedRestaurant.objects.filter(user=user).values_list('restaurant', flat=True)
    if not saved_restaurants:
        return Response([])

    saved_restaurant_objs = Restaurant.objects.filter(id__in=saved_restaurants)
    all_restaurants = Restaurant.objects.exclude(id__in=saved_restaurants)
    
    all_data = [
        f"{r.menu1} {r.menu2}  {r.service} {r.category} {r.location}"
        for r in all_restaurants
    ]

    saved_data = [
        f"{r.menu1} {r.menu2} {r.service} {r.category} {r.location}"
        for r in saved_restaurant_objs
    ]

    vectorizer = CountVectorizer().fit_transform(saved_data + all_data)
    vectors = vectorizer.toarray()
    cosine_matrix = cosine_similarity(vectors)

    saved_indices = range(len(saved_data))
    similar_indices = cosine_matrix[saved_indices, len(saved_data):].mean(axis=0).argsort()[::-1][:5]
    similar_indices = [int(i) for i in similar_indices]  # int64를 int로 변환
    similar_restaurants = [all_restaurants[i] for i in similar_indices]

    serializer = RestaurantSerializer(similar_restaurants, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def save_restaurant(request):
    user = request.user
    restaurant_id = request.data.get('id')
    restaurant = Restaurant.objects.get(id=restaurant_id)
    SavedRestaurant.objects.get_or_create(user=user, restaurant=restaurant)
    return Response({'status': 'saved'})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unsave_restaurant(request):
    user = request.user
    restaurant_id = request.data.get('id')
    restaurant = Restaurant.objects.get(id=restaurant_id)
    SavedRestaurant.objects.filter(user=user, restaurant=restaurant).delete()
    return Response({'status': 'unsaved'})
