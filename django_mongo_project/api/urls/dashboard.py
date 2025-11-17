from django.urls import path
from api.views.dashboard import get_dashboard_statistics

urlpatterns = [
    path('statistics/', get_dashboard_statistics, name='get_dashboard_statistics'),
]
