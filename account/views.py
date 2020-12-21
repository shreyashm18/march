from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404 , JsonResponse
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.views import APIView 
from .serializers import RegisterSerializer, loginserializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.decorators import login_required

from .models import User_country
from covid.models import country_code

# Create your views here.

def home(request):
    cnt = country_code.objects.all()
    return render(request,'home.html',{'cnt':cnt})


class getUser(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request):
        user = User.objects.all()
        serialize = RegisterSerializer(user, many = True)
        return JsonResponse(serialize.data , safe = False ,status = 200)

class RegisterUser(APIView):
    # serializer_class = RegisterSerializer
    

    def get(self,request):
        return render(request,'register.html')

    def post(self,request):
        country = request.POST['country']
        serialize = RegisterSerializer(data=request.POST)
        if serialize.is_valid():
            serialize.save()
            usr = User_country.objects.get(user_name=request.POST['username'])
            usr.country = country
            usr.save() 
            # return JsonResponse(serialize.data ,status = 201)
            return redirect('home')
        return JsonResponse(serialize.errors , status = 400)

from django.contrib.auth import login, logout
from rest_framework.authtoken.models import Token
from rest_framework.response import Response


class LogIn(APIView):

    def get(self,request):
        if request.user.is_authenticated:
            return redirect('home')
        return render(request,'login.html')
    
    def post(self,request):
        data=request.data
        serializer=loginserializer(data=data)
        serializer.is_valid(raise_exception=True)
        user=serializer.validated_data['user']
        login(request,user)
        if request.GET.get('next', None):
            return redirect(request.GET["next"])
        
        token,created=Token.objects.get_or_create(user=user)
        # return Response({'Token is':token.key},status=200)
        return redirect('home')


class LogOut(APIView):
    # authentication_classes=[TokenAuthentication]

    def get(self,request):
        logout(request)
        # return Response(status=204)
        return redirect('home')

