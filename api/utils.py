def get_age_group(age):
    if age <= 12:
        return "child"
    elif age <= 19:
        return "teenager"
    elif age <= 59:
        return "adult"
    return "senior"

COUNTRY_MAP = {
    "nigeria": "NG",
    "kenya": "KE",
    "angola": "AO",
    "ghana": "GH",
    "ethiopia": "ET",
    "tanzania": "TZ",
    "south africa": "ZA",
    "egypt": "EG",
    "cameroon": "CM",
    "ivory coast": "CI",
    "senegal": "SN",
    "benin": "BJ",
    "togo": "TG",
    "mali": "ML",
    "niger": "NE",
    "chad": "TD",
    "sudan": "SD",
    "somalia": "SO",
    "mozambique": "MZ",
    "zambia": "ZM",
    "zimbabwe": "ZW",
    "rwanda": "RW",
    "uganda": "UG",
    "united states": "US",
    "usa": "US",
    "united kingdom": "GB",
    "uk": "GB",
    "france": "FR",
    "germany": "DE",
    "brazil": "BR",
    "india": "IN",
    "china": "CN",
    "japan": "JP",
    "canada": "CA",
    "australia": "AU",
}

COUNTRY_ID_TO_NAME = {v: k.title() for k, v in COUNTRY_MAP.items()}
COUNTRY_ID_TO_NAME.update({
    "NG": "Nigeria", "KE": "Kenya", "AO": "Angola", "GH": "Ghana",
    "ET": "Ethiopia", "TZ": "Tanzania", "ZA": "South Africa", "EG": "Egypt",
    "CM": "Cameroon", "CI": "Ivory Coast", "SN": "Senegal", "BJ": "Benin",
    "TG": "Togo", "ML": "Mali", "NE": "Niger", "TD": "Chad",
    "SD": "Sudan", "SO": "Somalia", "MZ": "Mozambique", "ZM": "Zambia",
    "ZW": "Zimbabwe", "RW": "Rwanda", "UG": "Uganda",
    "US": "United States", "GB": "United Kingdom", "FR": "France",
    "DE": "Germany", "BR": "Brazil", "IN": "India", "CN": "China",
    "JP": "Japan", "CA": "Canada", "AU": "Australia",
})
