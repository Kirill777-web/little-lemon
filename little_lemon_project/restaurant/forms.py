from django.forms import ModelForm
from .models import Booking


# Creating BookingForm

class BookingForm(ModelForm):
    class Meta:
        model = Booking
        fields = "__all__"
