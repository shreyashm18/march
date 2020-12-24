from django.urls import path
from .views import ReportByCountry , passToken , GetBarChart#, UpdateCountryCodeDataBase
urlpatterns = [
    path('report/', ReportByCountry.as_view(),name = 'corona_report'),
    path('passtoken/', passToken,name = 'passtoken'),
    path('barchart/', GetBarChart.as_view(),name = 'barchart'),
    # path('updatecode/', UpdateCountryCodeDataBase.as_view(),name = 'updatecode'),
    
]
