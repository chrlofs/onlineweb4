from django.forms import ModelForm
from apps.meetapp.models import Meeting

class CreateNewMeetingForm(ModelForm):
    class Meta:
        model = Meeting
        fields = ['title', 'date']
