from django.contrib import admin
from .models import Booking, Kayak, Route, TermKayaks, DateList, BookingDate, FAQ, PrivacyPolicy


class BookingTermKayakInLine(admin.TabularInline):
    model = TermKayaks
    raw_id_fields = ['kayak']


class BookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'code', 'first_name', 'last_name', 'user', 'route', 'booking_date', 'time', 'phone', 'email', 'exact_time']
    inlines = [BookingTermKayakInLine]


class KayakAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'stock', 'store', 'type', 'available', 'prize']


class RouteAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'distance', 'average_time', 'stop_place', 'next_stage']


admin.site.register(Route, RouteAdmin)
admin.site.register(Booking, BookingAdmin)
admin.site.register(Kayak, KayakAdmin)
admin.site.register(DateList)
admin.site.register(BookingDate)
admin.site.register(FAQ)
admin.site.register(PrivacyPolicy)



