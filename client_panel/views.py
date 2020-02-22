from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from client_panel.forms import BookingCreateForm, SignUpCreateForm
from client_panel.models import Booking


class BookingCreateView(CreateView):
    model = Booking
    template_name = 'booking/create.html'
    form_class = BookingCreateForm

    def form_valid(self, form):
        return super(BookingCreateView, self).form_valid(form)


class SignUpCreateView(CreateView):
    model = UserCreationForm
    template_name = 'registration/signup_form.html'
    form_class = SignUpCreateForm

    def form_valid(self, form):
        return super(SignUpCreateView, self).form_valid(form)

