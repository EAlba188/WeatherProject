from django.template.response import TemplateResponse
from django.views import View
from django.shortcuts import redirect
from django.urls import reverse
from mainapp.API import get_city_data
from mainapp.services import trim_data_by_hour, create_csv
from django.shortcuts import render
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from django.http import HttpResponse
import io
import pandas as pd
from threading import RLock
verrou = RLock()


class MainView(View):
    template = "main_view.html"

    def get(self, request):
        post_mode = False
        return TemplateResponse(request, self.template, {"post_mode": post_mode})

    def post(self, request):
        template = "graphs.html"
        post_mode = True
        city = request.POST.get("city", None)
        start_date = request.POST.get("start_date", None)
        end_date = request.POST.get("end_date", None)
        start_hour = request.POST.get("start_hour", None)
        end_hour = request.POST.get("end_hour", None)

        if start_date > end_date or start_hour > end_hour:
            post_mode = False
            return TemplateResponse(request, self.template, {"post_mode": post_mode, "error": True})

        choose = f"You have choose to check {city} city in the dates between {start_date} and {end_date}" \
                 f" between {start_hour} and {end_hour} hours."

        city_data_json = get_city_data(city, start_date, end_date)
        trimed_data_by_hour = trim_data_by_hour(city_data_json, start_hour, end_hour)
        request.session["data_for_csv"] = trimed_data_by_hour

        return TemplateResponse(request, template, {"post_mode": post_mode,
                                                         "choose": choose,
                                                         "trimed_data_by_hour": trimed_data_by_hour})


class CSVDownloadView(View):

    def get(self, request):
        data = request.session["data_for_csv"]
        response = create_csv(data)
        return response


def heatmap_month_vs_hour(request):

    with verrou:
        data = request.session["data_for_csv"]
        df = pd.DataFrame({'Time': data['new_time'],
                           'Temperature': data['new_temperature_2m'],
                           'Rain': data["new_rain"],
                           'cloudcover': data["new_cloudcover"],
                           'windspeed_10m': data["new_windspeed_10m"],
                           'winddirection_10m': data["new_winddirection_10m"]})

        df['Time'] = pd.to_datetime(df['Time'])
        df['hour'] = df['Time'].dt.hour
        df['month'] = df['Time'].dt.month

        df_temp = df.groupby(['month', 'hour'])['Temperature'].mean().unstack()

        plt.figure()
        ax = sns.heatmap(df_temp, cmap='RdBu_r', vmin=df['Temperature'].min(), vmax=df['Temperature'].max())

        fig = plt.gcf()
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close(fig)
        response = HttpResponse(buf.getvalue(), content_type='image/png')
        return response


def heatmap_week_vs_hour(request):

    with verrou:
        data = request.session["data_for_csv"]
        df = pd.DataFrame({'Time': data['new_time'],
                           'Temperature': data['new_temperature_2m'],
                           'Rain': data["new_rain"],
                           'cloudcover': data["new_cloudcover"],
                           'windspeed_10m': data["new_windspeed_10m"],
                           'winddirection_10m': data["new_winddirection_10m"]})

        df['Time'] = pd.to_datetime(df['Time'])
        df['hour'] = df['Time'].dt.hour
        df['week'] = df['Time'].dt.isocalendar().week

        df_temp = df.groupby(['week', 'hour'])['Temperature'].mean().unstack()

        plt.figure()
        ax = sns.heatmap(df_temp, cmap='RdBu_r', vmin=df['Temperature'].min(), vmax=df['Temperature'].max())

        fig = plt.gcf()
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close(fig)
        response = HttpResponse(buf.getvalue(), content_type='image/png')
        return response