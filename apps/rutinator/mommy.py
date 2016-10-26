# -*- coding: utf-8 -*-

import logging

from django.utils import timezone

from .models import Task as rutinatorTask
from .send_mail import send_email
from apps.mommy import schedule
from apps.mommy.registry import Task
from .signals import new_membership_approval_handler


class RutinatorMail(Task):
    @staticmethod
    def run():
        logger = logging.getLogger("rutinator")
        logger.info("Rutinator job started")
        rutinator_tasks = rutinatorTask.objects.filter(deadline__gte=timezone.now())

        for task in rutinator_tasks:
            send_email(task)


schedule.register(RutinatorMail, day_of_week='mon-sun', hour=8, minute=0)
