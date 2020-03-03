from django.contrib import admin
from .models import Booking, Kayak, Route, BookingKayaks, Term


class BookingKayakInLine(admin.TabularInline):
    model = BookingKayaks
    raw_id_fields = ['kayak']


class BookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'user', 'route', 'date', 'time']
    inlines = [BookingKayakInLine]

admin.site.register(Booking, BookingAdmin)


class KayakAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'store', 'type', 'available', 'description']

admin.site.register(Kayak, KayakAdmin)
admin.site.register(Term)


class RouteAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'distance', 'description']

admin.site.register(Route, RouteAdmin)



