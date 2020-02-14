from django.shortcuts import render
from django.views.generic import CreateView
from client_panel.forms import BookingCreateForm
from client_panel.models import Booking


class BookingCreateView(CreateView):
    model = Booking
    template_name = 'booking/create.html'
    form_class = BookingCreateForm

    def form_valid(self, form):
        return super(BookingCreateView, self).form_valid(form)
