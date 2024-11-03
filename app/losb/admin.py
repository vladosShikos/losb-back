from __future__ import annotations

from django.contrib import admin
from losb.models import User, Phone, City, SMSVerification


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(Phone)
class PhoneAdmin(admin.ModelAdmin):
    pass


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    pass


@admin.register(SMSVerification)
class SMSVerificationAdmin(admin.ModelAdmin):
    pass
