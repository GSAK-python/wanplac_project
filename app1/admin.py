from django.contrib import admin
from app1.models import DailyKayakBooking, DailyKayak, Route, Booking, Term


# class DailyKayakBookingInLine(admin.TabularInline):
#     model = DailyKayakBooking
#     raw_id_fields = ['amount']
#     max_num = 4
#
#
# class BookingAdmin(admin.ModelAdmin):
#     list_display = ['id', 'first_name', 'last_name', 'user', 'route', 'time']
#     inlines = [DailyKayakBookingInLine]
#
#
# admin.site.register(DailyKayak)
# admin.site.register(Route)
# admin.site.register(Booking, BookingAdmin)
# admin.site.register(Term)
