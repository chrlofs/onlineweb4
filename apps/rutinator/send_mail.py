# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib import auth, messages
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.template.loader import render_to_string
from django.utils.translation import ugettext as _


def send_email(task):
    try:
        if task.user.get_email:
            email_context = {}
            email_context['email'] = task.user.get_email().email
            email_context['username'] = task.user.username
            email_context['task'] = task

            email_message = render_to_string('rutinator/email/mail.txt', email_context)

            send_mail(_("[rutinator] " + task.title), email_message, settings.DEFAULT_FROM_EMAIL, [email_context['email']])
    except:
        print("Ingen mail-konto knyttet til denne profilen")
