# Create your views here.
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from apps.meetapp.forms import CreateNewMeetingForm


@login_required
def index(request, active_tab='agenda'):
    context = {}
    context['active_tab'] = active_tab
    return render(request, 'meetapp/index.html', context)


@login_required
def create_meeting(request):

    if request.method == 'POST':
        if not CreateNewMeetingForm.is_valid():
            messages.error(request, 'Noen av de påkrevde feltene mangler')
        else:
            CreateNewMeetingForm.save()
            messages.success(request, 'Møtet ble opprettet')

    return redirect(index, active_tab='fravaer')
