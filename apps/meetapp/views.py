# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def index(request):
    context = {}
    return render(request, 'meetapp/index.html', context)
