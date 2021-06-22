from django.contrib import admin
from .models import User, Address


class UserAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email']


class AddressAdmin(admin.ModelAdmin):
    list_display = ['postal_code', 'municipality', 'state', 'user', 'primary']


admin.site.register(User, UserAdmin)
admin.site.register(Address, AddressAdmin)
