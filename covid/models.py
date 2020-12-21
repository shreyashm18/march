from django.db import models

# Create your models here.
class country_code(models.Model):
    country = models.TextField(max_length=500)
    code = models.CharField(max_length=25)

    def __str__(self):
        return self.country