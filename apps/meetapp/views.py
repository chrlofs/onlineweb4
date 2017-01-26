# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def index(request, active_tab='agenda'):
    context = {}
    context['active_tab'] = active_tab
    return render(request, 'meetapp/index.html', context)
