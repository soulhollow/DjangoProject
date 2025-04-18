# ai_assistant/urls.py
from django.urls import path
from . import api

urlpatterns = [
    path('contacts/<int:contact_id>/lead-score/', api.calculate_lead_score, name='lead-score'),
    path('contacts/<int:contact_id>/follow-up-suggestions/', api.get_follow_up_suggestions,
         name='follow-up-suggestions'),
]