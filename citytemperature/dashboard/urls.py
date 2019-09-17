from django.conf.urls import url
from . import views

app_name='dashboard'

urlpatterns = [ 
	url(r'^$',views.dashboard,name='dashboard'),
	url(r'^city/$',views.city_list,name='city'),
	url(r'^data/$',views.dashboard,name='dashboard'),
	url(r'^filter/$',views.get_filter_data,name='filter_data')
]