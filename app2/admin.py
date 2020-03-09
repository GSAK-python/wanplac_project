from django.contrib import admin

from app2.models import BookingKayaks, TermKayaks, Route, Booking, Kayak, Term


class BookingKayakInLine(admin.TabularInline):
    model = BookingKayaks
    raw_id_fields = ['date']
    max_num = 1


class BookingTermKayakInLine(admin.TabularInline):
    model = TermKayaks
    raw_id_fields = ['kayak']


class BookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'user', 'route', 'time']
    inlines = [BookingKayakInLine, BookingTermKayakInLine]


class KayakAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'store', 'type', 'available', 'description']


class RouteAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'distance', 'description']


admin.site.register(Route, RouteAdmin)
admin.site.register(Booking, BookingAdmin)
admin.site.register(Kayak, KayakAdmin)
admin.site.register(Term)
