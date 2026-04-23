from django.urls import path
from .views import create_profile, get_profile, get_profiles, delete_profile, search_profiles

urlpatterns = [
    path('profiles', create_profile),
    path('profiles/search', search_profiles),
    path('profiles/all', get_profiles),
    path('profiles/<uuid:id>', get_profile),
    path('profiles/<uuid:id>/delete', delete_profile),
]
