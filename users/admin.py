from django.contrib import admin

from users.models import User, EmailVerification
from products.admin import BasketAdmin


# admin.site.register(User)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username',)
    inlines = (BasketAdmin,)


@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = ('code', 'user', 'expiration')
    fields = ('code', 'user', 'expiration', 'created_at')
    readonly_fields = ('created_at',)
