# Generated by Django 3.0.1 on 2020-12-20 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_auto_20201220_1957'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_country',
            name='user_name',
            field=models.CharField(default='kaka', max_length=256),
        ),
    ]
