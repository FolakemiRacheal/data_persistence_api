from django.urls import path
from .views import create_profile, get_profile, get_profiles, delete_profile

urlpatterns = [
    path('profiles', create_profile),
    path('profiles/all', get_profiles),
    path('profiles/<uuid:id>', get_profile),
    path('profiles/<uuid:id>/delete', delete_profile),
]