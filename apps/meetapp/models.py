from django.db import models


class Meeting(models.Model):
    title = models.CharField(max_length=50)
    date = models.DateTimeField('meeting_start')
