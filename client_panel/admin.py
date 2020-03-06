from django.contrib import admin
from .models import Booking, Kayak, Route, BookingKayaks, Term, TermKayaks, DailyKayak, DailyKayakBooking


class BookingKayakInLine(admin.TabularInline):
    model = BookingKayaks
    raw_id_fields = ['date']
    max_num = 1


class BookingTermKayakInLine(admin.TabularInline):
    model = TermKayaks
    raw_id_fields = ['kayak']


class DailyKayakBookingInLine(admin.TabularInline):
    model = DailyKayakBooking
    raw_id_fields = ['amount']
    max_num = 4


class BookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'user', 'route', 'time']
    inlines = [DailyKayakBookingInLine, BookingKayakInLine, BookingTermKayakInLine]


class KayakAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'store', 'type', 'available', 'description']


class RouteAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'distance', 'description']


admin.site.register(Route, RouteAdmin)
admin.site.register(Booking, BookingAdmin)
admin.site.register(Kayak, KayakAdmin)
admin.site.register(Term)
admin.site.register(DailyKayak)


