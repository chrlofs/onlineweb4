# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import ugettext as _

from apps.dashboard.widgets import DatetimePickerInput, multiple_widget_generator
from apps.events.models import AttendanceEvent, Event, Reservation
from apps.payment.models import Payment


class EventForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = (
            'title', 'event_type', 'event_start', 'event_end', 'location', 'ingress_short', 'ingress', 'description',
            'image'
        )

        dtp_fields = [('event_start', {}), ('event_end', {})]

        widgetlist = [
            (DatetimePickerInput, dtp_fields)
        ]

        # Multiple widget generator merges results from regular widget_generator into a single widget dict
        widgets = multiple_widget_generator(widgetlist)


class AttendanceEventForm(forms.ModelForm):
    active = forms.BooleanField(required=False)
    prefix = 'attendance'

    class Meta:
        model = AttendanceEvent
        fields = (
            'max_capacity', 'waitlist', 'guest_attendance',
            'registration_start', 'registration_end', 'unattend_deadline',
            'automatically_set_marks', 'rule_bundles',
        )

        dtp_fields = [('registration_start', {}), ('registration_end', {}), ('unattend_deadline', {})]

        widgetlist = [
            (DatetimePickerInput, dtp_fields)
        ]

        # Multiple widget generator merges results from regular widget_generator into a single widget dict
        widgets = multiple_widget_generator(widgetlist)


class PaymentForm(forms.ModelForm):
    active = forms.BooleanField(required=False)
    prefix = 'payment'

    def clean(self):
        cleaned_data = super(PaymentForm, self).clean()
        type = cleaned_data.get("payment_type")
        deadline = cleaned_data.get("deadline")
        delay = cleaned_data.get("delay")

        if type == 2 and not deadline:
            self.add_error('deadline', _("Fristen må fylles ut"))

        if type == 3 and not delay:
            self.add_error('delay', _("Utsettelse må være utfylt"))

    class Meta:
        model = Payment
        fields = (
            'stripe_key', 'payment_type', 'deadline', 'active', 'delay'
        )

        dtp_fields = [('deadline', {}),]

        widgetlist = [
            (DatetimePickerInput, dtp_fields)
        ]

        # Multiple widget generator merges results from regular widget_generator into a single widget dict
        widgets = multiple_widget_generator(widgetlist)


class ChangeReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        exclude = ['attendance_event', ]
