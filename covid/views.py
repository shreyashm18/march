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
import json
from .calculations import get_last_15_days, get_by_date_range

from . import barchart
from django.contrib import messages

def passToken(request, time_period = 15):
    print(f'request = {request.user}')
    token = Token.objects.get(user=request.user)
    print(f'token = {token.key}')
    print(f'request from passToken = {request.GET}')
    
    form = InputDataForm(request.GET)
    if not form.is_valid():
        return render(request, 'home.html', { 'form':form })

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
    authentication_classes = [TokenAuthentication,SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self,request, time_period = 15):
        
        # print(request.user.username)
        # print(f'data from post method {request.POST}')
        
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
            dict = get_last_15_days(data=data,timeline=timeline,time_period=time_period,country=country)
        else:
            dict = get_by_date_range(data=data,timeline=timeline,country=country,start_date=start_date,end_date=end_date)
        
        # return render(request,'covid.html',dict)
        return Response(dict)
from .gmailAPI import sendEmail
class GetBarChart(APIView):

    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request):
        return render(request,'barchart.html')
    def post(self,request):
        mail_id = request.POST['email']
        print(f"entered email {request.POST['email']}")
        endpoint = " https://corona-api.com/countries"
        resp = requests.get(endpoint)
        resp = resp.json()
        pic_location = barchart.plot(resp=resp,mail_id=mail_id)
        # print(pic_location)
        try:
            sendEmail.connect_method(mail_id=mail_id,pic_location=pic_location)
        except:
            messages.error(request, 'Error Detected')
            return redirect('barchart')
        else:
            messages.info(request,'Mail sent')
        return redirect('home')

'''Below code I had written just to insert country name and their code in database '''

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