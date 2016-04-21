from django.shortcuts import render
from django.shortcuts import render_to_response
from models import *
from django.template import Context, loader
from django.http import HttpResponse
import datetime
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from models import MyModel 
from django.contrib.auth.models import User
import json
import copy
from braces import views as braces_views
from annoying.decorators import render_to
from django.core import serializers

def qdict_to_dict(qdict):
    """Convert a Django QueryDict to a Python dict.

    Single-value fields are put in directly, and for multi-value fields, a list
    of all values is stored at the field's key.

    """
    return {k: v[0] if len(v) == 1 else v for k, v in qdict.lists()}

def helloworld(request, vehicle_type):
    data = {'foo': 'bar', 'hello': 'world'}
    if request.method == 'POST':
        return HttpResponse(json.dumps({'success': True}))
    #return HttpResponse(json.dumps(data))   
    else:
        countries = Country.objects.all()
        dict1 = {'countries': countries}
        return render_to_response('helloworld.html', dict1 ,context_instance=RequestContext(request))
# Create your views here.


#@login_required(login_url= 'google')
def SomeView(request, vehicle_type):
    template_name = 'helloworld.html'
    return render_to_response(template_name, context_instance=RequestContext(request))


class BaseMixin(braces_views.JSONResponseMixin, braces_views.AjaxResponseMixin):
    
    def dispatch(self, *args, **kwargs):
        self.vehicle_type = self.vehicle_type or self.kwargs.get('vehicle_type', '')
        self.mapped_vehicle_type = {
            'fourwheeler': 'Private Car',
            'twowheeler': 'Twowheeler',
        }.get(self.vehicle_type, '')
        return super(BaseMixin, self).dispatch(*args, **kwargs)

    def get_ajax(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def post_ajax(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


def Question(request):
    request_data =  copy.deepcopy(request.POST)
    pass

def country_list(request, vehicle_type):
    if request.method =="POST":
        countries = Country.objects.all()
        return HttpResponse(countries)


def cities(request, vehicle_type):
    if request.method=="POST":
        request_data = copy.deepcopy(request.POST)
        request_data = qdict_to_dict(request_data)
        cities = City.objects.filter(country_id=request_data['jobID'])
        data = serializers.serialize('json', cities)
        return HttpResponse(data, content_type='application/json')