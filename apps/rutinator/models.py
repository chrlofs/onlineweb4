from django.conf import settings
from django.db import models
from django.contrib.auth.models import User, Group

import random

User = settings.AUTH_USER_MODEL


class Task(models.Model):

    TYPE_CHOICES = (
        (1, ('En gang')),
        (2, ('Gjentagende')),
    )

    title = models.CharField(u"Tittel", max_length=45)
    description = models.CharField(u"Oppgave", max_length=100)
    completed = models.BooleanField(u"Ferdigstilt", default=False)
    completed_date = models.DateTimeField(u"Ferdigstilt dato", blank=True, null=True)
    deadline = models.DateTimeField(u"Tidsfrist", blank=True, null=True)
    group = models.ForeignKey(Group, blank=False, null=True, verbose_name='Ansvarlig gruppe')
    user = models.ForeignKey(User, blank=True, null=True, verbose_name='Ansvarlig person')
    choose_random = models.BooleanField()
    task_type = models.SmallIntegerField((u'Type'), choices=TYPE_CHOICES, default=1)


    def random_from_group(self):
        user = random.choice(self.group.user_set.all())



    # send mail (see mommy)


def __unicode__(self):
    return self.title
