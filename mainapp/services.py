import datetime
import pandas as pd
from django.http import HttpResponse


# Remove the data from the dataset to return only the hours requested frame
def trim_data_by_hour(data, start_hour, end_hour):

    hours = data["hourly"]["time"]

    start_hour = datetime.datetime.strptime(start_hour, "%H:%M").time()
    end_hour = datetime.datetime.strptime(end_hour, "%H:%M").time()

    hours = [datetime.datetime.strptime(hora, "%Y-%m-%dT%H:%M").time() for hora in hours]

    non_requested_hours = [hour for hour in hours if not start_hour <= hour <= end_hour]

    positions_to_remove = [i for i, hora in enumerate(hours) if hora in non_requested_hours]

    new_time = remove_positions(data["hourly"]["time"], positions_to_remove)
    new_temperature_2m = remove_positions(data["hourly"]["temperature_2m"], positions_to_remove)
    new_rain = remove_positions(data["hourly"]["rain"], positions_to_remove)
    new_cloudcover = remove_positions(data["hourly"]["cloudcover"], positions_to_remove)
    new_windspeed_10m = remove_positions(data["hourly"]["windspeed_10m"], positions_to_remove)
    new_winddirection_10m = remove_positions(data["hourly"]["winddirection_10m"], positions_to_remove)

    trimed_dict = {
        "new_time": new_time,
        "new_temperature_2m": new_temperature_2m,
        "new_rain": new_rain,
        "new_cloudcover": new_cloudcover,
        "new_windspeed_10m": new_windspeed_10m,
        "new_winddirection_10m": new_winddirection_10m
    }

    return trimed_dict


def remove_positions(data_list, indexes):
    new_lst = [j for i, j in enumerate(data_list) if i not in indexes]
    return new_lst


def create_csv(data):
    print(data["new_time"])
    df = pd.DataFrame({'Time': data['new_time'],
                       'Temperature': data['new_temperature_2m'],
                       'Rain': data["new_rain"],
                       'cloudcover': data["new_cloudcover"],
                       'windspeed_10m': data["new_windspeed_10m"],
                       'winddirection_10m': data["new_winddirection_10m"]})

    csv_data = df.to_csv(index=False)

    response = HttpResponse(csv_data, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="csv_data_generated.csv"'

    return response


