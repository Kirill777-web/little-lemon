from datetime import datetime
import json
from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers
from .models import Booking

from django.views.decorators.csrf import csrf_exempt

from django.http import Http404
from django.shortcuts import render, redirect
from .forms import BookingForm, CommentForm
from .models import Menu, UserComments
import traceback

# Create your views here.


def home(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def reservations(request):
    date = request.GET.get('date', datetime.today().date())
    bookings = Booking.objects.all()
    booking_json = serializers.serialize('json', bookings)
    return render(request, 'bookings.html', {"bookings": booking_json})


def book(request):
    form = BookingForm()
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'book.html', context)


def menu(request):
    menu_data = Menu.objects.all()
    main_data = {"menu": menu_data}
    return render(request, 'menu.html', main_data)


def display_menu_items(request, pk=None):
    if pk:
        try:
            menu_item = Menu.objects.get(pk=pk)
        except Menu.DoesNotExist:
            raise Http404("Menu item does not exist")
    else:
        menu_item = ''
    return render(request, 'menu_item.html', {'menu_item': menu_item})


# Booking View

@csrf_exempt
def bookings(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            reservation_slot = datetime.strptime(
                data['reservation_slot'], '%H:%M').time()
        except ValueError:
            return JsonResponse({'success': False, 'error': 'Invalid time format. It must be in HH:MM format.'})

        exist = Booking.objects.filter(
            reservation_date=data['reservation_date'],
            reservation_slot=reservation_slot
        ).exists()

        if not exist:
            booking = Booking(
                first_name=data['first_name'],
                last_name=data['last_name'],
                guest_number=data['guest_number'],
                reservation_date=data['reservation_date'],
                reservation_slot=reservation_slot,
            )
            booking.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'Reservation already exists for this time slot.'})

    date = request.GET.get('date', datetime.today().date())
    bookings = Booking.objects.filter(reservation_date=date)
    booking_list = [{
        'first_name': b.first_name,
        'last_name': b.last_name,
        'guest_number': b.guest_number,
        'reservation_date': b.reservation_date.isoformat(),
        'reservation_slot': b.reservation_slot.strftime('%H:%M'),
    } for b in bookings]
    return JsonResponse(booking_list, safe=False)

# Comments View


def form_view(request):
    form = CommentForm()

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            uc = UserComments(
                first_name=cd['first_name'],
                last_name=cd['last_name'],
                comment=cd['comment'],
            )
            uc.save()
            return JsonResponse({'message': 'success'})
    return render(request, 'blog.html', {'form': form})
