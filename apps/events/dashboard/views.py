# -*- coding: utf-8 -*-

from collections import OrderedDict
from datetime import datetime, time, timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.forms.models import modelformset_factory
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.translation import ugettext as _
from guardian.decorators import permission_required

from apps.dashboard.tools import get_base_context, has_access
from apps.events.dashboard.forms import (AttendanceEventForm, EventForm,
                                         ChangeReservationForm, PaymentForm)
from apps.events.dashboard.utils import event_ajax_handler
from apps.events.models import AttendanceEvent, Attendee, Event, Reservation, Reservee
from apps.events.utils import get_group_restricted_events, get_types_allowed
from apps.payment.models import PaymentRelation


@login_required
@permission_required('events.view_event', return_403=True)
def index(request):
    if not has_access(request):
        raise PermissionDenied

    allowed_events = get_group_restricted_events(request.user, True)
    events = allowed_events.filter(event_start__gte=timezone.now().date()).order_by('event_start')

    context = get_base_context(request)
    context['events'] = events

    return render(request, 'events/dashboard/index.html', context)


@login_required
@permission_required('events.view_event', return_403=True)
def past(request):
    if not has_access(request):
        raise PermissionDenied

    allowed_events = get_group_restricted_events(request.user, True)
    events = allowed_events.filter(event_start__lt=timezone.now().date()).order_by('-event_start')

    context = get_base_context(request)
    context['events'] = events

    return render(request, 'events/dashboard/index.html', context)


@login_required
@permission_required('events.view_event', return_403=True)
def create_event(request):
    if not has_access(request):
        raise PermissionDenied

    context = get_base_context(request)

    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            cleaned = form.cleaned_data

            if cleaned['event_type'] not in get_types_allowed(request.user):
                messages.error(request, _(
                    "Du har ikke tilgang til å lage arranngement av typen '%s'.") % cleaned['event_type'])
                context['change_event_form'] = form

            else:
                # Create object, but do not commit to db. We need to add stuff.
                event = form.save(commit=False)
                # Add author
                event.author = request.user
                event.save()

                messages.success(request, _("Arrangementet ble opprettet."))
                return redirect('dashboard_event_details', event_id=event.id)

        else:
            context['change_event_form'] = form

    if 'change_event_form' not in context.keys():
        context['change_event_form'] = EventForm()

    context['event'] = _('Nytt arrangement')
    context['active_tab'] = 'details'

    return render(request, 'events/dashboard/details.html', context)

class FormTemplate(object):

    def __init__(self, id, name, hidden=True):
        self.id = id
        self.name = name
        self.hidden = hidden




def edit_event(request, event_id):
    if not has_access(request):
        raise PermissionDenied

    context = get_base_context(request)

    event = get_object_or_404(Event, pk=event_id)
    context['event'] = event
    context['menu_items'] = _menu_items(event)

    if request.method == 'POST':
        forms = []

        main_form = EventForm(request.POST, instance=event)
        forms.append(main_form)

        attendance_form = _get_attendance_form(request, event)

        if attendance_form:
            forms.append(attendance_form)

        payment_form = _get_payment_form(request, event)

        if payment_form:
            forms.append(payment_form)

        forms_valid = True

        for form in forms:
            if not form.is_valid():
                forms_valid = False

        if not forms_valid:
            context['forms'] = _create_forms(event, forms)
            messages.error(request, "Noen felt inneholder feil.")
            return render(request, 'events/dashboard/edit.html', context)

        print(len(forms))

        for form in forms:
            if isinstance(form, EventForm):
                event_form = form.save(commit=False)
                event_form.author = request.user
                event_form.save()
            elif isinstance(form, AttendanceEventForm):
                attendance_form = form.save(commit=False)
                attendance_form.event = event
                attendance_form.save()
            elif isinstance(form, PaymentForm):
                payment_form = form.save(commit=False)
                payment_form.content_object = event.attendance_event
                payment_form.save()
            else:
                form.save()

        messages.success(request, _("Arrangementet ble endret."))

    context['forms'] = _create_forms(event)
    return render(request, 'events/dashboard/edit.html', context)

def _menu_items(event):
    attendance_item = {'id': 'add-attendance', 'name': 'Påmelding'}
    payment_item = {'id': 'add-payment', 'name': 'Betaling'}

    if event.is_attendance_event():
        attendance_item['disabled'] = True
        attendance_item['tooltip'] = "Det er kun mulig med en påmelding per event."

    if event.is_attendance_event() and event.attendance_event.payment():
        payment_item['tooltip'] = "Det er kun mulig med en betaling per event."
        payment_item['disabled'] = True
    elif not event.is_attendance_event():
        payment_item['tooltip'] = "Betaling krever et påmeldingsarrangement"
        payment_item['disabled'] = True

    menu_items = []
    menu_items.append(attendance_item)
    menu_items.append(payment_item)

    return menu_items

def _get_attendance_form(request, event):
    if event.is_attendance_event():
        return AttendanceEventForm(request.POST, instance=event.attendance_event)
    else:
        attendance_form = AttendanceEventForm(request.POST)

        if attendance_form['active'].value():
            return attendance_form

    return None

def _get_payment_form(request, event):
    if event.is_attendance_event() and event.attendance_event.payment():
        return PaymentForm(request.POST, instance=event.attendance_event.payment())
    else:
        payment_form = PaymentForm(request.POST)

        if payment_form['active'].value():
            return payment_form

    return None

def _create_forms(event, forms=None):

    event_form = FormTemplate("event", _("Arrangement"))
    attendance_form = FormTemplate("attendance", _("Påmelding"))
    payment_form = FormTemplate("payment", _("Betaling"))

    if forms:
        selected_set = False

        for form in forms:
            if isinstance(form, EventForm):
                form_template = event_form
            elif isinstance(form, AttendanceEventForm):
                form_template = attendance_form
            elif isinstance(form, PaymentForm):
                form_template = payment_form

            form_template.form = form
            form_template.hidden = False
            if not form.is_valid() and not selected_set:
                print(form)
                form_template.selected = True
                selected_set = True

        if not selected_set:
            event_form.selected = True
    else:
        event_form.selected = True
        event_form.form = EventForm(instance=event)

        if event.is_attendance_event():
            attendance_form.form = AttendanceEventForm(instance=event.attendance_event)
            attendance_form.hidden = False
        else:
            attendance_form.form = AttendanceEventForm()

        if event.is_attendance_event() and event.attendance_event.payment():
            payment_form.form = PaymentForm(instance=event.attendance_event.payment())
            payment_form.hidden = False
        else:
            payment_form.form = PaymentForm()


    forms = []
    forms.append(event_form)
    forms.append(attendance_form)
    forms.append(payment_form)

    return forms

def _payment_prices(attendance_event):
    payments = {}
    summary = OrderedDict()

    payment = attendance_event.payment()

    if payment and len(payment.prices()) > 1:

        for price in payment.prices():
            summary[price] = 0

        summary["Ikke valgt"] = 0

        for attendee in attendance_event.attendees_qs:
            paymentRelation = PaymentRelation.objects.filter(
                payment=attendance_event.payment(),
                user=attendee.user,
                refunded=False
            )

            if paymentRelation:
                payments[attendee] = paymentRelation[0].payment_price
                summary[paymentRelation[0].payment_price] += 1
            else:
                payments[attendee] = "-"
                summary['Ikke valgt'] += 1

    return (payments, summary)


@login_required
@permission_required('events.view_attendanceevent', return_403=True)
def event_change_attendance(request, event_id):
    context = _create_details_context(request, event_id)
    context['active_tab'] = 'attendance'

    event = context['event']

    if not event.is_attendance_event():
        registration_start = datetime.combine(event.event_start - timedelta(days=7), time(12, 0, 0))
        timezone.make_aware(registration_start, timezone.get_current_timezone())
        unattend_deadline = registration_start + timedelta(days=5)
        registration_end = registration_start + timedelta(days=6)

        attendance_event = AttendanceEvent(
            event=event,
            max_capacity=0,
            registration_start=registration_start,
            unattend_deadline=unattend_deadline,
            registration_end=registration_end
        )
        attendance_event.save()
        context['change_attendance_form'] = AttendanceEventForm(instance=event.attendance_event)

    else:
        if request.method == 'POST':
            form = AttendanceEventForm(request.POST, instance=event.attendance_event)
            if form.is_valid():
                form.save()
                messages.success(request, _("Påmeldingsdetaljer ble lagret."))
            context['change_attendance_form'] = form

    return render(request, 'events/dashboard/details.html', context)


@login_required
@permission_required('events.view_event', return_403=True)
def event_details(request, event_id, active_tab='attendees'):
    if not has_access(request):
        raise PermissionDenied

    context = get_base_context(request)
    context['active_tab'] = active_tab

    event = get_object_or_404(Event, pk=event_id)

    if not event.is_attendance_event():
        messages.error(request, _("Dette er ikke et påmeldingsarrangement."))
        return redirect('dashboard_event_details_active', event_id=event.id, active_tab='details')

    # AJAX
    if request.method == 'POST':
        if request.is_ajax and 'action' in request.POST:
            if not event.is_attendance_event:
                return HttpResponse(_('Dette er ikke et påmeldingsarrangement.'), status=400)

            return JsonResponse(event_ajax_handler(event, request))

    extras = {}
    if event.is_attendance_event() and event.attendance_event.extras:
        for extra in event.attendance_event.extras.all():
            extras[extra] = {"type": extra, "attending": 0, "waits": 0, "allergics": []}

        count_extras(extras, "attending", event.attendance_event.attendees_qs)
        count_extras(extras, "waits", event.attendance_event.waitlist_qs)

    if event.is_attendance_event():
        prices = _payment_prices(event.attendance_event)
        context['payment_prices'] = prices[0]
        context['payment_price_summary'] = prices[1]

    context['extras'] = extras

    return render(request, 'events/dashboard/details.html', context)


def count_extras(event_extras, attendance_list, attendees):
    for attendee in attendees:
        choice = attendee.extras
        if attendee.extras not in event_extras:
            event_extras[choice] = {"type": choice, "attending": 0, "waits": 0, "allergics": []}
        ex = event_extras[choice]
        ex[attendance_list] += 1
        if attendee.user.allergies:
            what_list = "påmeldt" if attendance_list is "attending" else "venteliste"
            ex["allergics"].append({"user": attendee.user, "list": what_list})


@login_required
@permission_required('events.view_reservation', return_403=True)
def event_change_reservation(request, event_id):
    if not has_access(request):
        raise PermissionDenied

    context = _create_details_context(request, event_id)
    context['active_tab'] = 'reservation'

    event = context['event']

    if not event.is_attendance_event():
        messages.error(request, _("Dette er ikke et påmeldingsarrangement."))
        return redirect('dashboard_event_details_active', event_id=event.id, active_tab='details')

    if request.method == 'POST':
        if not event.attendance_event.has_reservation:
            reservation = Reservation(
                attendance_event=event.attendance_event,
                seats=0
            )
            reservation.save()
            context['change_reservation_form'] = ChangeReservationForm(instance=reservation)
        else:
            form = ChangeReservationForm(request.POST, instance=event.attendance_event.reserved_seats)
            if form.is_valid():
                messages.success(request, _("Reservasjonen ble lagret."))
                form.save()
            context['change_reservation_form'] = form

    return render(request, 'events/dashboard/details.html', context)


@login_required
@permission_required('events.view_attendee', return_403=True)
def attendee_details(request, attendee_id):

    context = get_base_context(request)

    attendee = get_object_or_404(Attendee, pk=attendee_id)

    context['attendee'] = attendee
    return render(request, 'events/dashboard/attendee.html', context)
