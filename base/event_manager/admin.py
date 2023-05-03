from django.contrib import admin
from .models import CustomUser, Event

class CustomUserAdmin(admin.ModelAdmin):
    model = CustomUser

class EventAdmin(admin.ModelAdmin):
    model = Event
    list_display = ( 'name', 'start_date', 'end_date', 'owner' )


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Event, EventAdmin)