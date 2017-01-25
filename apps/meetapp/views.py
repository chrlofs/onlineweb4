# Create your views here.
from django.http import Http404, HttpResponse

def index(request):
	return HttpResponse("Hello World")