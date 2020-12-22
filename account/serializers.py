from rest_framework import serializers
from django.contrib.auth.models import User
from django import forms


class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    
    class Meta:
        model = User
        fields = ['first_name','last_name','username','email','password','password2']
        extra_kwargs = {
				'password': {'write_only': True},
		}

    def	save(self):

        account = User(
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
            email=self.validated_data['email'],
            username=self.validated_data['username']
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match.'})
        account.set_password(password)
        account.save()
        return account

from rest_framework import exceptions
from django.contrib.auth import authenticate

class loginserializer(serializers.Serializer):
    username=serializers.CharField()
    password=serializers.CharField()

    def validate(self,data):
        username=data.get('username')
        password=data.get('password')

        if username and password:
            user=authenticate(username=username,password=password)
            if user:
                if user.is_active:
                    data['user']=user
                else:
                    raise exceptions.ValidationError('User account is not active')
            else:
                raise exceptions.ValidationError('account not found')    
        else:
            raise exceptions.ValidationError('You should provide username and password')
        return data
