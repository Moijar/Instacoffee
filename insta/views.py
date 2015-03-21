from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response

# Create your views here.
def index(request):
    return render_to_response('index.html', {}, context_instance=RequestContext(request))
    #return HttpResponse("Hello, wld.")
