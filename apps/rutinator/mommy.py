# -*- coding: utf-8 -*-

import locale
import logging

from django.conf import settings
from django.core.mail import EmailMessage
from django.utils import timezone

from .models import Task
from .views import send_email
from apps.mommy import schedule
from apps.mommy.registry import Task


class RutinatorMail(Task):
    @staticmethod
    def run():
        logger = logging.getLogger("rutinator")
        logger.info("Rutinator job started")
        locale.setlocale(locale.LC_ALL, "nb_NO.UTF-8")
        rutinator_tasks = Task.objects.filter(deadline__gte=timezone.now())

        for task in rutinator_tasks:
            send_email(task)


schedule.register(RutinatorMail, day_of_week='mon-sun', hour=22, minute=50)
