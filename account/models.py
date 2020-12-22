from django.db import models
from django.contrib.auth.models import User
from covid.models import country_code

from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.
class User_country(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=256,null=False,blank=False,default="kaka")
    country = models.CharField(max_length=256,null=False,blank=False)

    def __str__(self):
        return self.user_name

@receiver(post_save, sender = User)
def country(sender, instance, created, **kwargs):
    print(f'instance is = {instance}')
    print(f'created = {created}')
    if created:
        User_country.objects.create(user = instance, user_name= str(instance))
    # else:
    #     instance.User_country.save()

class CountryList(models.Model):
    country = models.CharField(max_length=256)

    def __str__(self):
        return self.country