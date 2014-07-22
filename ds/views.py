from django.shortcuts import render

import json
from django.core import serializers
from django.http import HttpResponseRedirect, HttpResponse

from ds.models import Ziroom_House as Z

from django.shortcuts import render_to_response

def index(request):
    return render_to_response('index.html')


def list(request):
	ser = serializers.serialize('json', Z.objects.all(), fields=('lng', 'lat'))
	return HttpResponse(ser)


def render_to_json_response(context, **response_kwargs):
    data = json.dumps(context)
    response_kwargs['content_type'] = 'application/json'
    return HttpResponse(data, **response_kwargs)
