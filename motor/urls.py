from django.conf.urls import url, patterns
from django.views.generic.base import TemplateView
import views

urlpatterns = [
	url(r'^helloworld/$', views.helloworld, name = 'helloworld'),
    url(r'^countries', views.country_list, name = "get_countries"),
    url(r'^cities', views.cities, name = "get_cities")
	]



