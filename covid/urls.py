from django.urls import path
from .views import ReportByCountry , UpdateCountryCodeDataBase #, passToken #, UpdateCountryCodeDataBase
urlpatterns = [
    path('report/', ReportByCountry.as_view(),name = 'corona_report'),
    # path('passtoken/', passToken,name = 'passtoken'),
    path('updatecode/', UpdateCountryCodeDataBase.as_view(),name = 'updatecode'),
    
]
