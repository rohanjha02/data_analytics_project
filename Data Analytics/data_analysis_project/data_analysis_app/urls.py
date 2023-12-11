# data_analysis_app/urls.py
from django.urls import path
from .views import data_tab, descriptive_statistics_tab, exploratory_data_analysis_tab, predict, report, profile_view, export_to_csv, export_to_excel

urlpatterns = [
    path('data/', data_tab, name='data_tab'),
    path('descriptive-statistics/', descriptive_statistics_tab, name='descriptive_statistics_tab'),
    path('exploratory-data-analysis/', exploratory_data_analysis_tab, name='exploratory_data_analysis_tab'),
    path('predict/', predict, name='predict'),
    path('report/', report, name='report'),
    path('profile/', profile_view, name='profile_view'),
    path('export/csv/', export_to_csv, name='export_to_csv'),
    path('export/excel/', export_to_excel, name='export_to_excel'),
]