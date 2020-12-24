from datetime import datetime, timedelta

def get_last_15_days(data,timeline,time_period,country):
        
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

def get_by_date_range(data,timeline,country,start_date,end_date):
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