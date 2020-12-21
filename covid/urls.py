from django.urls import path
from .views import ReportByCountry #, UpdateCountryCodeDataBase
urlpatterns = [
    path('report/', ReportByCountry.as_view(),name = 'corona_report'),
    # path('updatecode/', UpdateCountryCodeDataBase.as_view(),name = 'updatecode'),
    
]
