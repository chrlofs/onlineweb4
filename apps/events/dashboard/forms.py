# -*- coding: utf-8 -*-

from django import forms
from django.forms import BaseModelFormSet
from django.utils.translation import ugettext as _

from apps.dashboard.widgets import DatetimePickerInput, multiple_widget_generator
from apps.events.models import AttendanceEvent, Event, Reservation
from apps.payment.models import Payment, PaymentPrice


class EventForm(forms.ModelForm):

    prefix = "event"
    name = "Arrangement"
    selected = False

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
    name = "Påmelding"
    selected = False
    hidden = True

    def menu_condition(event):
        if event.is_attendance_event():
           return "Det er kun mulig med en påmelding per event."

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
    name = "Betaling"
    selected = False
    hidden = True
    price_forms = []

    def menu_condition(event):
        if event.is_attendance_event() and event.attendance_event.payment():
            return "Det er kun mulig med en betaling per event."
        elif not event.is_attendance_event():
            return "Betaling krever et påmeldingsarrangement"

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


class PaymentPriceModelFormSet(BaseModelFormSet):
    def clean(self):
        super(PaymentPriceModelFormSet, self).clean()

        multiple_forms = len(self.forms) > 1

        #TODO generate error

        for form in self.forms:
            if multiple_forms and not form.cleaned_data['description']:
               raise forms.ValidationError('Beskrivelse må være utfylt når det finnes flere priser')



class ChangeReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        exclude = ['attendance_event', ]
