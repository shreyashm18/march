from django.shortcuts import render, redirect

from django.http import response
from rest_framework.views import APIView
from rest_framework.response import Response
import requests
from datetime import datetime, timedelta
from rest_framework import generics
from .models import country_code
from rest_framework.authentication import TokenAuthentication
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from rest_framework.authtoken.models import Token
from account.models import User_country, CountryList

# def passToken(request):
#     print(f'request = {request.user}')
#     token = Token.objects.get(user=request.user)
#     print(f'token = {token.key}')
#     print(f'token type = {type(token.key)}')
#     # token = token.key
#     if token.key:
#         endpoint = 'http://127.0.0.1:8000/covid/report/'
#         tkn = 'Token '+token.key
#         dict = requests.post(url=endpoint, headers = {'Authorization': tkn})
#     return redirect('home')


class ReportByCountry(APIView):
    
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    
    def get(self,request, time_period = 15):

        print(request.user.username)
        # print(f'form data {request.GET}')
        # country = (CountryList.objects.get(id = request.GET['country'])).country
        # print(f"country == {country}")
        # print(f"type of country == {type(country)}")
        
        endpoint = "http://corona-api.com/countries/"
        if request.GET.get('country'):
            country = (CountryList.objects.get(id = request.GET['country'])).country
        else:
            try:
                cnt=User_country.objects.get(user_name=request.user.username)
                country = cnt.country
            except User_country.DoesNotExist:
                return redirect('home')
        if request.GET.get('days'):
            time_period = int(request.GET['days'])
        print(f'time_period = {time_period}')
        print(f'country = {country}')
        country_name = country_code.objects.get(country = country)
        print(f'country code = {country_name.code}')
        resp = requests.get(endpoint+country_name.code)
        resp = resp.json()

        data = resp['data']

        today = datetime.today().date()
        timeline = data['timeline']
        time_period = today - timedelta(days=time_period)

        latest_data = data['latest_data']
        calculated = latest_data['calculated']

        dict ={'country':country,'Total_patients':latest_data['confirmed'],'Total_recovered':latest_data['recovered'],
                'new_confirmed':0,'new_recovered':0,'total_death':latest_data['deaths'],'new_deaths':0,'active_patient':latest_data['critical'],
                'death_rate':calculated['death_rate'],'recovery_rate':calculated['recovery_rate'],'cases_per_million_population':calculated['cases_per_million_population']}
        
        for i in timeline:
            new_date = i.get('date')
            new_date = datetime.strptime(new_date,'%Y-%m-%d').date()
            if not new_date < time_period:
                # print(i.get('date'))
                dict['new_confirmed'] += i.get('new_confirmed')
                dict['new_recovered'] += i.get('new_recovered')
                dict['new_deaths'] += i.get('new_deaths')
                # print("\n")
        print(dict)

        return render(request,'covid.html',dict)
        # return redirect('home')


class UpdateCountryCodeDataBase(APIView):
    # authentication_classes = [TokenAuthentication]
    authentication_classes = [SessionAuthentication,BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request):
        endpoint = 'https://corona-api.com/countries'
        response = requests.get(url=endpoint)
        # print(response.url)
        resp = response.json()
        
        for country in resp['data']:
            try:
                country_name = country_code.objects.get(country = country['name'])
                if not country_name.code == country['code']:
                    country_name.code = country['code']
                    country_name.save()
            except country_code.DoesNotExist:
                country_name = country_code.objects.create(country = country['name'], code = country['code'])
                country_name.save()
                cnt = CountryList.objects.create(country=country['name'])
                cnt.save()
        return redirect('home')