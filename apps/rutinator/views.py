from django.shortcuts import render, get_object_or_404, redirect

from onlineweb4.apps.events.utils import get_group_restricted_events
from .models import Task

from apps.authentication.models import OnlineUser as User, RegisterToken, Email

# Create your views here.

from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect


def send_email(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    subject = request.POST.get('subject', 'Dette er en påminnelse om en rutineoppgave')
    message = request.POST.get('message', 'Dette er en automatisk påminnelse om oppgaven: {}!'.format(task.title))
    from_email = request.POST.get('from_email', '')
    if subject and message and from_email:
        try:
            send_mail(subject, message, from_email, [''])
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
        return HttpResponseRedirect("")
    else:
        # In reality we'd use a form class
        # to get proper validation errors.
        return HttpResponse('Make sure all fields are entered and valid.')



# Forsett her:
# https://docs.djangoproject.com/en/1.10/topics/email/
