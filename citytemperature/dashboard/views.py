from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import City , Temperature
from django.http import JsonResponse,HttpResponse
from django.db.models import Avg
import json


@login_required(login_url="/accounts/login/")
def dashboard(request):

    cities = City.objects.order_by().values_list('city_name', flat=True).distinct()

    years = Temperature.objects.order_by().values_list('year', flat=True).distinct()

    temperatures = Temperature.objects.values('city__city_name','year').annotate(temperature = Avg('temperature'))
    
    years_list =Temperature.objects.values('year').annotate(temperature = Avg('temperature'))

    result =list( Temperature.objects.values('city__city_name').annotate(temperature = Avg('temperature')))



    city_list_data =[]
    year_list_data =[]
    temp_list_data =[]
    temp_avg_by_city =[]

    temp_l=[]
    for entry in result:
        
        json_obj = dict(
            name = entry['city__city_name'],
            y = entry['temperature'],
            drilldown = entry['city__city_name']

        )
        temp_l.append(json_obj)

    drilldown_series = {}
    for bana in temperatures:
        if bana['city__city_name'] in drilldown_series:
            drilldown_series[bana['city__city_name']].append([bana['year'],bana['temperature']])
        else:
            drilldown_series[bana['city__city_name']]=[]
            drilldown_series[bana['city__city_name']].append([bana['year'],bana['temperature']])

    drilldown_series_1 = []
    city_temp = Temperature.objects.values('city__city_name').distinct()
    for bana in city_temp:
        drilldown_series_1.append({
        'name':bana['city__city_name'],
        'type':'line',
        'id':bana['city__city_name'],
        'data':drilldown_series[bana['city__city_name']]
        })

    for entry in result:
        city_list_data.append(entry['city__city_name'])
        temp_avg_by_city.append(entry['temperature'])
    for entry in years_list:
        year_list_data.append(entry['year'])
    for entry in years_list:
        temp_list_data.append(entry['temperature'])   


    context = {
                'cities':cities,
                'years': years,
                'temperatures':temperatures,
                'years_list':json.dumps(year_list_data),
                'temp_avg_by_city':json.dumps(temp_avg_by_city),
                'temp_list':json.dumps(temp_list_data),
                'city_list':json.dumps(city_list_data),
                'city_temp_year':json.dumps(temp_l),
                'drilldown_series_1':json.dumps(drilldown_series_1)

            }
    return render(request,'dashboard/dashboard.html',context)


@login_required(login_url="/accounts/login/")
def city_list(request):
    city = City.objects.all()
    return render(request,'dashboard/city_list.html',{'city':city})

@login_required(login_url="/accounts/login/")
def get_filter_data(request):

    cities=request.POST.getlist('filter_city_list[]')
    years=request.POST.getlist('filter_year_list[]')

    # print(years)
    
    year_list_data =[]
    temp_avg_by_year =[]
    cities_list_data =[]
    temp_avg_by_city =[]

    #To get average temperature -By year -By City 
    years_list =Temperature.objects.filter(year__in=years).values('year').annotate(temperature = Avg('temperature'))
    city_list =Temperature.objects.filter(city__city_name__in=cities).values('city__city_name').annotate(temperature = Avg('temperature'))
    city_l = Temperature.objects.filter(city__city_name__in=cities).filter(year__in=years).values('city__city_name','year','temperature') 
    years_avg = Temperature.objects.filter(city__city_name__in=cities).filter(year__in=years).values('city__city_name').annotate(temperature = Avg('temperature'))

    for entry in years_list:
        year_list_data.append(entry['year'])
        temp_avg_by_year.append(entry['temperature'])

    for entry in city_list:
        cities_list_data.append(entry['city__city_name'])
        temp_avg_by_city.append(entry['temperature'])

    temp_l=[]
    for entry in years_avg:
        
        json_obj = dict(
            name = entry['city__city_name'],
            y = entry['temperature'],
            drilldown = entry['city__city_name']

        )
        temp_l.append(json_obj)
    # print(temp_l)
    drilldown_series = {}
    for bana in city_l:
        if bana['city__city_name'] in drilldown_series:
            drilldown_series[bana['city__city_name']].append([bana['year'],bana['temperature']])
        else:
            drilldown_series[bana['city__city_name']]=[]
            drilldown_series[bana['city__city_name']].append([bana['year'],bana['temperature']])
    # print(drilldown_series)



    drilldown_series_1 = []
    for bana in city_list:
        drilldown_series_1.append({
        'name':bana['city__city_name'],
        'type':'line',
        'id':bana['city__city_name'],
        'data':drilldown_series[bana['city__city_name']]
        })

    # print("drillllllllllll",drilldown_series_1)
    context ={
        'year_list_data':json.dumps(year_list_data),
        'temp_avg_by_year':json.dumps(temp_avg_by_year),
        'temp_l':json.dumps(temp_l),
        'drilldown_series_1':json.dumps(drilldown_series_1)

    }

    return HttpResponse(json.dumps(context))


    
