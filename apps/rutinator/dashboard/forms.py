from django import forms
from apps.rutinator.models import Task
from apps.dashboard.widgets import DatetimePickerInput, multiple_widget_generator

class NewTaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = (
            'title',
            'description',
            'deadline',
            'group',
            'task_type'
        )




