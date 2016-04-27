from django import forms
from apps.rutinator.models import Task
from django.utils import timezone
from apps.dashboard.widgets import DatetimePickerInput, multiple_widget_generator

class NewTaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = (
            'title',
            'description',
            'group',
            'user',
            'task_type',
            'deadline'
        )

        test = [('deadline', {'placeholder': 'Velg ...'})]

        widgetlist = [
            (DatetimePickerInput, test),
        ]

        widgets = multiple_widget_generator(widgetlist)



