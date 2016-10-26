from django import forms
from apps.rutinator.models import Task
from django.utils import timezone
from apps.dashboard.widgets import DatetimePickerInput, multiple_widget_generator
import random

from django.contrib.auth.models import User, Group


class NewTaskForm(forms.ModelForm):

    class Meta:
        def __init__(self, task_list, *args, **kwargs):
            super(NewTaskForm, self).__init__(*args, **kwargs)
            # print dir(self.fields['list'])
            # print self.fields['list'].initial
            self.fields['assigned_to'].queryset = User.objects.filter(groups__in=[task_list.group])
            self.fields['assigned_to'].label_from_instance = \
                lambda obj: "%s (%s)" % (obj.get_full_name(), obj.username)

        due_date = forms.DateField(
            required=False,
            widget=forms.DateTimeInput(attrs={'class': 'due_date_picker'})
        )

        model = Task
        fields = (
            'title',
            'description',
            'group',
            'user',
            'task_type',
            'deadline',
            'choose_random'
        )

        test = [('deadline', {'placeholder': 'Velg ...'})]

        widgetlist = [
            (DatetimePickerInput, test),
        ]

        widgets = multiple_widget_generator(widgetlist)



