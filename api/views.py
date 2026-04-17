from django.shortcuts import render

# Create your views here.
import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Profile
from .serializers import ProfileSerializer
from .utils import get_age_group

@api_view(['GET', 'POST'])
def create_profile(request):
    if request.method == 'GET':
        return get_profiles(request._request)

    name = request.data.get('name')

    if not name:
        return Response({"status": "error", "message": "Name is required"}, status=400)

    if not isinstance(name, str):
        return Response({"status": "error", "message": "Invalid type"}, status=422)

    name = name.lower()

    existing = Profile.objects.filter(name=name).first()
    if existing:
        return Response({
            "status": "success",
            "message": "Profile already exists",
            "data": ProfileSerializer(existing).data
        })

    try:
       
        gender_res = requests.get(f"https://api.genderize.io?name={name}").json()
        age_res = requests.get(f"https://api.agify.io?name={name}").json()
        country_res = requests.get(f"https://api.nationalize.io?name={name}").json()

        if gender_res.get("gender") is None or gender_res.get("count") == 0:
            return Response({"status": "error", "message": "Genderize returned an invalid response"}, status=502)

        if age_res.get("age") is None:
            return Response({"status": "error", "message": "Agify returned an invalid response"}, status=502)

        countries = country_res.get("country", [])
        if not countries:
            return Response({"status": "error", "message": "Nationalize returned an invalid response"}, status=502)

        top_country = max(countries, key=lambda x: x["probability"])

        age = age_res["age"]
        age_group = get_age_group(age)

        profile = Profile.objects.create(
            name=name,
            gender=gender_res["gender"],
            gender_probability=gender_res["probability"],
            sample_size=gender_res["count"],
            age=age,
            age_group=age_group,
            country_id=top_country["country_id"],
            country_probability=top_country["probability"]
        )

        return Response({
            "status": "success",
            "data": ProfileSerializer(profile).data
        }, status=201)

    except Exception:
        return Response({"status": "error", "message": "Server error"}, status=500)
    
@api_view(['GET'])
def get_profile(request, id):
    try:
        profile = Profile.objects.get(id=id)
        return Response({
            "status": "success",
            "data": ProfileSerializer(profile).data
        })
    except Profile.DoesNotExist:
        return Response({"status": "error", "message": "Profile not found"}, status=404)
    
@api_view(['GET'])
def get_profiles(request):
    profiles = Profile.objects.all()
    gender = request.GET.get('gender')
    country = request.GET.get('country_id')
    age_group = request.GET.get('age_group')
       
    if gender:
        profiles = profiles.filter(gender__iexact=gender)
    if country:
        profiles = profiles.filter(country_id__iexact=country)
    if age_group:
        profiles = profiles.filter(age_group__iexact=age_group)

    data = [
        {
            "id": p.id,
            "name": p.name,
            "gender": p.gender,
            "age": p.age,
            "age_group": p.age_group,
            "country_id": p.country_id
        }
        for p in profiles
    ]

    return Response({
        "status": "success",
        "count": len(data),
        "data": data
    })

@api_view(['DELETE'])
def delete_profile(request, id):
    try:
        profile = Profile.objects.get(id=id)
        profile.delete()
        return Response(status=204)
    except Profile.DoesNotExist:
        return Response({"status": "error", "message": "Profile not found"}, status=404)