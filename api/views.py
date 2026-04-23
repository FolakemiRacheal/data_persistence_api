import re
import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Profile
from .serializers import ProfileSerializer
from .utils import get_age_group, COUNTRY_MAP, COUNTRY_ID_TO_NAME

VALID_SORT_FIELDS = {"age", "created_at", "gender_probability"}

def _apply_filters_and_paginate(queryset, params):
    gender = params.get('gender')
    country_id = params.get('country_id')
    age_group = params.get('age_group')
    min_age = params.get('min_age')
    max_age = params.get('max_age')
    min_gender_prob = params.get('min_gender_probability')
    min_country_prob = params.get('min_country_probability')
    sort_by = params.get('sort_by')
    order = params.get('order', 'asc')

    if gender:
        queryset = queryset.filter(gender__iexact=gender)
    if country_id:
        queryset = queryset.filter(country_id__iexact=country_id)
    if age_group:
        queryset = queryset.filter(age_group__iexact=age_group)
    if min_age:
        queryset = queryset.filter(age__gte=min_age)
    if max_age:
        queryset = queryset.filter(age__lte=max_age)
    if min_gender_prob:
        queryset = queryset.filter(gender_probability__gte=min_gender_prob)
    if min_country_prob:
        queryset = queryset.filter(country_probability__gte=min_country_prob)

    if sort_by:
        if sort_by not in VALID_SORT_FIELDS:
            return None, {"status": "error", "message": "Invalid query parameters"}
        if order == 'desc':
            sort_by = f"-{sort_by}"
        queryset = queryset.order_by(sort_by)

    try:
        page = int(params.get('page', 1))
        limit = min(int(params.get('limit', 10)), 50)
    except (ValueError, TypeError):
        return None, {"status": "error", "message": "Invalid query parameters"}

    total = queryset.count()
    start = (page - 1) * limit
    data = ProfileSerializer(queryset[start:start + limit], many=True).data

    return {"status": "success", "page": page, "limit": limit, "total": total, "data": data}, None


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
        country_code = top_country["country_id"]

        age = age_res["age"]

        profile = Profile.objects.create(
            name=name,
            gender=gender_res["gender"],
            gender_probability=gender_res["probability"],
            sample_size=gender_res["count"],
            age=age,
            age_group=get_age_group(age),
            country_id=country_code,
            country_name=COUNTRY_ID_TO_NAME.get(country_code, country_code),
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
        return Response({"status": "success", "data": ProfileSerializer(profile).data})
    except Profile.DoesNotExist:
        return Response({"status": "error", "message": "Profile not found"}, status=404)


@api_view(['GET'])
def get_profiles(request):
    result, error = _apply_filters_and_paginate(Profile.objects.all(), request.GET)
    if error:
        return Response(error, status=400)
    return Response(result)


@api_view(['GET'])
def search_profiles(request):
    query = request.GET.get('q', '').strip()

    if not query:
        return Response({"status": "error", "message": "Missing query parameter"}, status=400)

    q = query.lower()
    filters = {}

    if re.search(r'\bfemale\b', q):
        filters["gender"] = "female"
    elif re.search(r'\bmale\b', q):
        filters["gender"] = "male"

   
    for group in ("child", "teenager", "adult", "senior"):
        if re.search(rf'\b{group}\b', q):
            filters["age_group"] = group
            break

  
    if re.search(r'\byoung\b', q):
        filters["min_age"] = 16
        filters["max_age"] = 24

   
    match = re.search(r'\babove\s+(\d+)\b', q)
    if match:
        filters["min_age"] = int(match.group(1))

    match = re.search(r'\bbelow\s+(\d+)\b', q)
    if match:
        filters["max_age"] = int(match.group(1))

    for country, code in COUNTRY_MAP.items():
        if re.search(rf'\b{re.escape(country)}\b', q):
            filters["country_id"] = code
            break

    if not filters:
        return Response({"status": "error", "message": "Unable to interpret query"}, status=422)

    params = {**filters, **request.GET.dict()}
    result, error = _apply_filters_and_paginate(Profile.objects.all(), params)
    if error:
        return Response(error, status=400)
    return Response(result)


@api_view(['DELETE'])
def delete_profile(request, id):
    try:
        profile = Profile.objects.get(id=id)
        profile.delete()
        return Response(status=204)
    except Profile.DoesNotExist:
        return Response({"status": "error", "message": "Profile not found"}, status=404)
