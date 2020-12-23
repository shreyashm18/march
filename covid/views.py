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
from account.forms import InputDataForm
from rest_framework import filters
import json


def passToken(request, time_period = 15):
    print(f'request = {request.user}')
    token = Token.objects.get(user=request.user)
    print(f'token = {token.key}')
    print(f'request from passToken = {request.GET}')
    
    data = {
        "country": request.GET['country'],
        "start_date": request.GET['start_date'], 
        "end_date": request.GET['end_date']
        }
    print(f'data to pass = {data}')
    # token = token.key
    if token.key:
        endpoint = 'http://127.0.0.1:8000/covid/report/'
        tkn = 'Token '+token.key
       
        dict = requests.post(url=endpoint, headers = {'Authorization': tkn},data=data)
        dict = dict.json()
        print(f'tookeenn = {tkn}')
        print(f'dict = {dict} dict type = {type(dict)}')
    return render(request,'covid.html',dict)


class ReportByCountry(APIView):
    queryset = Token.objects.all()
    authentication_classes = [TokenAuthentication] #,SessionAuthentication
    # permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['key']

    def get_last_15_days(self,data,timeline,time_period,country):
        
        today = datetime.today().date()
        print(f'time period = {time_period}')
        time_period = today - timedelta(days=time_period)
        latest_data = data['latest_data']
        calculated = latest_data['calculated']

        dict ={'country':country,'Total_patients':latest_data['confirmed'],'Total_recovered':latest_data['recovered'],
                'new_confirmed':0,'new_recovered':0,'total_death':latest_data['deaths'],'new_deaths':0,'active_patient':latest_data['critical'],
                'death_rate':calculated['death_rate'],'recovery_rate':calculated['recovery_rate'],
                'cases_per_million_population':calculated['cases_per_million_population'],'msg':''}
        
        for i in timeline:
            new_date = i.get('date')
            new_date = datetime.strptime(new_date,'%Y-%m-%d').date()
            if not new_date < time_period:
                # print(i.get('date'))
                dict['new_confirmed'] += i.get('new_confirmed')
                dict['new_recovered'] += i.get('new_recovered')
                dict['new_deaths'] += i.get('new_deaths')
            # print("\n")
        return dict

    def get_by_date_range(self,data,timeline,country,start_date,end_date):
        dict ={'country':country,'Total_patients':0,'Total_recovered':0,'new_confirmed':0,'new_recovered':0,'total_death':0,'new_deaths':0,
            'active_patient':0,'death_rate':0,'recovery_rate':0,'start_date':start_date,'end_date':end_date,'msg':f" (till {end_date})"}
        
        start_date = datetime.strptime(start_date,'%Y-%m-%d').date()
        end_date = datetime.strptime(end_date,'%Y-%m-%d').date()
        count = 0

        for i in timeline:
            new_date = i.get('date')
            new_date = datetime.strptime(new_date,'%Y-%m-%d').date()
            
            if not (new_date < start_date or new_date > end_date):
                # print(i.get('date'))
                if count == 0:
                    dict['Total_patients'] = i.get('confirmed') 
                    dict['Total_recovered'] = i.get('recovered')
                    dict['total_death'] = i.get('deaths')
                dict['new_confirmed'] += i.get('new_confirmed')
                dict['new_recovered'] += i.get('new_recovered')
                dict['new_deaths'] += i.get('new_deaths')
                count += 1
        print(dict)
        print(count)
        dict['active_patient'] = dict['Total_patients'] - dict['Total_recovered'] - dict['total_death']
        dict['death_rate'] = (dict['total_death'] / dict['Total_patients']) * 100
        dict['recovery_rate'] = (dict['Total_recovered'] / dict['Total_patients']) * 100
        return dict
        
    
    def post(self,request, time_period = 15):
        
        # print(request.user.username)
        # print(f'data from post method {request.POST}')

        form = InputDataForm(request.POST)
        if not form.is_valid():
            return render(request, 'home.html', { 'form':form })
        
        endpoint = "http://corona-api.com/countries/"
        if request.POST.get('country'):
            country = (CountryList.objects.get(id = request.POST['country'])).country
        else:
            try:
                cnt=User_country.objects.get(user_name=request.user.username)
                country = cnt.country
            except User_country.DoesNotExist:
                return redirect('home')

        date_status = False
        if request.POST.get('start_date'):
            start_date = request.POST['start_date']
            date_status = True
            if request.POST.get('end_date'):
                end_date = request.POST['end_date']
            else:
                end_date = datetime.today().date()
            print(f'start date = {start_date} end date = {end_date}')
        
        country_name = country_code.objects.get(country = country)
        print(f'country name post = {country}\n country code post = {country_name.code}')
        resp = requests.get(endpoint+country_name.code)
        resp = resp.json()
        data = resp['data']
        timeline = data['timeline']

        if not date_status:
            dict = self.get_last_15_days(data=data,timeline=timeline,time_period=time_period,country=country)
        else:
            dict = self.get_by_date_range(data=data,timeline=timeline,country=country,start_date=start_date,end_date=end_date)
        ###########################################################################
        # return render(request,'covid.html',dict)
        # return redirect('home')
        return Response(dict)

# class UpdateCountryCodeDataBase(APIView):
#     # authentication_classes = [TokenAuthentication]
#     authentication_classes = [SessionAuthentication,BasicAuthentication]
#     permission_classes = [IsAuthenticated]

#     def get(self,request):
#         endpoint = 'https://corona-api.com/countries'
#         response = requests.get(url=endpoint)
#         # print(response.url)
#         resp = response.json()
        
#         for country in resp['data']:
#             try:
#                 country_name = country_code.objects.get(country = country['name'])
#                 if not country_name.code == country['code']:
#                     country_name.code = country['code']
#                     country_name.save()
#             except country_code.DoesNotExist:
#                 country_name = country_code.objects.create(country = country['name'], code = country['code'])
#                 country_name.save()
#                 cnt = CountryList.objects.create(country=country['name'])
#                 cnt.save()
#         return redirect('home')