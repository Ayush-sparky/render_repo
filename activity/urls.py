from django.urls import path
from .views import ActivityListCreateView, CarbonFootprintView, LeaderboardView, ActivityByDateView,WeeklyActivityView, MonthlyActivityView

urlpatterns = [
    path('api/activities/', ActivityListCreateView.as_view(), name='activities'),
    path('api/carbon-footprint/', CarbonFootprintView.as_view(), name='carbon-footprint'),
    path('api/leaderboard/', LeaderboardView.as_view(), name='leaderboard'),
    path('api/activities/<str:date>/', ActivityByDateView.as_view(), name='activities-by-date'),
    path('api/activities/week/<str:date>/', WeeklyActivityView.as_view(), name='weekly-activities'),
    path('api/activities/month/<str:date>/', MonthlyActivityView.as_view(), name='monthly-activities'),
    
]