from django.forms import ModelForm
from .models import Booking, UserComments


# Creating BookingForm

class BookingForm(ModelForm):
    class Meta:
        model = Booking
        fields = "__all__"


class CommentForm(ModelForm):
    class Meta:
        model = UserComments
        fields = '__all__'
