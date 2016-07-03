# -*- coding: utf-8 -*-

from collections import OrderedDict
from datetime import datetime, time, timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.forms import formset_factory, modelformset_factory
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.translation import ugettext as _
from guardian.decorators import permission_required

from apps.dashboard.tools import get_base_context, has_access
from apps.events.dashboard.forms import (AttendanceEventForm, EventForm, ChangeReservationForm,
                                         PaymentForm, PaymentPriceModelFormSet)
from apps.events.dashboard.utils import event_ajax_handler
from apps.events.models import AttendanceEvent, Attendee, Event, Reservation, Reservee
from apps.events.utils import get_group_restricted_events, get_types_allowed
from apps.payment.models import PaymentRelation, PaymentPrice

PaymentPriceFormSet = modelformset_factory(
    PaymentPrice,
    extra=0,
    fields=('price', 'description'),
    min_num=1,
    can_delete=True,
    formset=PaymentPriceModelFormSet
)

enabled_forms = [
    EventForm,
    AttendanceEventForm,
    PaymentForm
]

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

def edit_event(request, event_id):
    if not has_access(request):
        raise PermissionDenied

    event = get_object_or_404(Event, pk=event_id)

    context = get_base_context(request)
    context['event'] = event
    context['menu_items'] = _menu_items(event)

    if request.method == 'POST':
        forms = _clean_forms(request, event)

        price_forms = _clean_formset(request, forms, event)

        forms_valid = _validate_forms(forms, price_forms)

        if not forms_valid:
            context['price_forms'] = price_forms
            context['forms'] = _set_active_form(forms, price_forms)
            messages.error(request, "Noen felt inneholder feil.")
            return render(request, 'events/dashboard/edit.html', context)

        _save_forms(request, event, forms, price_forms)
        messages.success(request, _("Arrangementet ble endret."))

    context['forms'] = _create_forms(event, context)
    return render(request, 'events/dashboard/edit.html', context)

def _menu_items(event):
    menu_items = []

    for form in enabled_forms[1:]: #Skips the first element (EventForm)
        menu_item = {}
        menu_item['id'] = form.prefix
        menu_item['name'] = form.name
        menu_item['tooltip'] = form.menu_condition(event)
        menu_items.append(menu_item)

    return menu_items

def _create_forms(event, context):

    event_form = EventForm(instance=event)
    event_form.selected = True

    if event.is_attendance_event():
        attendance_form = AttendanceEventForm(instance=event.attendance_event)
        attendance_form.hidden = False
    else:
        attendance_form = AttendanceEventForm()

    if event.is_attendance_event() and event.attendance_event.payment():
        payment_form = PaymentForm(instance=event.attendance_event.payment())
        payment_form.hidden = False

        context['price_forms'] = PaymentPriceFormSet(queryset=event.attendance_event.payment().prices())
    else:
        payment_form = PaymentForm()
        context['price_forms'] = PaymentPriceFormSet(queryset=PaymentPrice.objects.none())


    #TODO add more forms

    forms = []
    forms.append(event_form)
    forms.append(attendance_form)
    forms.append(payment_form)

    return forms

def _clean_forms(request, event):
    forms = []
    forms.append(EventForm(request.POST, instance=event))

    _add_form(request, forms, event.attendance_event, AttendanceEventForm)
    _add_form(request, forms, event.attendance_event.payment(), PaymentForm)
    #TODO add more forms

    return forms

def _clean_formset(request, forms, event):

    if not any(isinstance(form, PaymentForm) for form in forms):
        return None

    if event.attendance_event.payment().prices():
        return PaymentPriceFormSet(request.POST, queryset=event.attendance_event.payment().prices())
    else:
        return PaymentPriceFormSet(request.POST)

def _add_form(request, forms, instance, Form):
    if instance:
        form = Form(request.POST, instance=instance)
        form.hidden = False
        forms.append(form)
    else:
        form = Form(request.POST)

        if form['active'].value():
            form.hidden = False
            forms.append(form)

# Validate all forms to present all errors to the user
def _validate_forms(forms, formset):
    valid = True

    if formset and not formset.is_valid():
        valid = False

    for form in forms:
        if not form.is_valid():
            valid = False

    return valid

def _set_active_form(forms, formset):

    selected_set = False

    for form in forms:
        form.selected = False

        if not form.is_valid() and not selected_set:
            form.selected = True
            selected_set = True

        if not selected_set and formset and not formset.is_valid() and form.prefix == "payment":
            form.selected = True
            selected_set = True

    if not selected_set:
        form[0].selected = True

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

def _save_forms(request, event, forms, price_forms):
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

    if price_forms:
        _save_price_forms(price_forms, event)

def _save_price_forms(price_forms, event):
    for price_form in price_forms:
        payment_price = price_form.save(commit=False)
        payment_price.payment = event.attendance_event.payment()
        payment_price.save()

    for form in price_forms.deleted_forms:
        payment_price = form.save(commit=False)
        # if payment_price.is_in_use:
        #     message.error(request, _("Kan ikke slette pris hvor noen har betalt."))
        #     return render(request, 'events/dashboard/edit.html', context)
        #TODO check if last price
        #TODO check if anyone has paid
        payment_price.delete()
