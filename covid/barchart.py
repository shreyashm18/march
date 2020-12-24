import requests
import json
import matplotlib.pyplot as plt
from django.conf import settings
import os
def plot(resp,mail_id):

    New_Colors = ['green','blue','purple','brown','teal','red']
    country = ['Australia','Germany','India','Japan','USA','UK']
    country_code = []
    confirmed = []
    recovered = []
    deaths = []
    critical = []
    per_million = []
    mail_list = mail_id.split('@')
    pic_name = 'covid_barchart_'+mail_list[0]
    f_name = '/'+pic_name + '.png'
    path=settings.MEDIA_ROOT
    pic_location = path+'barchart_images'+f_name
    # print(os.listdir(loc))
    for i in resp['data']:
        if i['name'] in country:
            country_code.append(i['code'])
            confirmed.append(i['latest_data']['confirmed'])
            recovered.append(i['latest_data']['recovered'])
            per_million.append(i['latest_data']['calculated']['cases_per_million_population'])
        # print(f"{i['name']}\t {i['latest_data']['confirmed']}")
    print(country)
    print(country_code)
    print(confirmed)
    print(recovered)

    plt.bar(country, per_million, color=New_Colors)
    plt.title('Country Vs COVID Cases per million', fontsize=14)
    plt.xlabel('Country', fontsize=14)
    plt.ylabel('Confirmed Cases per 1000000', fontsize=14)
    path=settings.MEDIA_ROOT
    plt.savefig(pic_location)
    return pic_location
    # plt.grid(True)
    # print(plt.show())