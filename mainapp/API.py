import requests
from ninja import NinjaAPI

api = NinjaAPI()

# Latitude longitude
Hamburg = [53.5507, 9.993]
Berlín = [52.5244, 13.4105]
Düsseldorf = [51.2217, 6.7762]
Frankfurt = [49.6833, 10.5333]
Múnich = [48.1374, 11.5755]


def get_data_from_api(latitude_longitude, start_date, end_date):
    url = f'https://archive-api.open-meteo.com/v1/archive?latitude={latitude_longitude[0]}&longitude={latitude_longitude[1]}&start_date={start_date}&end_date={end_date}&hourly=temperature_2m,rain,cloudcover,windspeed_10m,winddirection_10m&timezone=Europe%2FBerlin'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None


@api.get("/Get_City")
def get_city_data(city, start_date, end_date):
    if city == "Hamburg":
        city = Hamburg
    elif city == "Berlín":
        city = Berlín
    elif city == "Düsseldorf":
        city = Düsseldorf
    elif city == "Frankfurt":
        city = Frankfurt
    elif city == "Múnich":
        city = Múnich
    else:
        pass
        # TODO RETURN ERROR
    # TODO Check date correct format year month day

    return get_data_from_api(city, start_date, end_date)
