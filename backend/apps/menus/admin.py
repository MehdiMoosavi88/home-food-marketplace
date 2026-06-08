from django.contrib import admin

from .models import (
    Menu,
    MenuItem,
    MenuItemAvailability
)

admin.site.register(Menu)
admin.site.register(MenuItem)
admin.site.register(MenuItemAvailability)