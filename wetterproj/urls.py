from django.contrib import admin
from django.urls import path
from mainapp.API import api
from mainapp.views import MainView, CSVDownloadView, heatmap_month_vs_hour, heatmap_week_vs_hour

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", api.urls),
    path("main_view/", MainView.as_view(), name="main_view"),
    path("csv_download/", CSVDownloadView.as_view(), name="csv_download"),
    path('heatmap_month_vs_hour/', heatmap_month_vs_hour, name='heatmap_month_vs_hour'),
    path('heatmap_week_vs_hour/', heatmap_week_vs_hour, name='heatmap_week_vs_hour'),
]