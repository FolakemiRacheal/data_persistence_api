import json
from api.models import Profile


def run():
    with open('seed_profiles.json') as f:
        data = json.load(f)

    profiles = data if isinstance(data, list) else data.get('profiles', [])
    created = 0

    for item in profiles:
        obj, is_created = Profile.objects.get_or_create(
            name=item["name"],
            defaults={
                "gender": item["gender"],
                "gender_probability": item["gender_probability"],
                "sample_size": item.get("sample_size", 0),
                "age": item["age"],
                "age_group": item["age_group"],
                "country_id": item["country_id"],
                "country_name": item["country_name"],
                "country_probability": item["country_probability"],
            }
        )

        if is_created:
            created += 1

    print(f"{created} profiles added (duplicates skipped)")