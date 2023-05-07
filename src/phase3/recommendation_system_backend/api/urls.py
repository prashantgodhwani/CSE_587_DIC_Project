from django.urls import path
from . import views

urlpatterns = [
 path('explore-beyond/', views.exploreTheBeyondRecommendations,),
 path('best-nearby/', views.bestNearbyRecommendations),
 path('top-places/', views.topPlacesRecommendations),
 path('feeling-lucky/', views.feelingLuckyRecommendations),
 path('feedback/submit-review/', views.submitReview),
]