from django.contrib import admin

from users.models import Balance


class BalanceAdmin(admin.ModelAdmin):
    list_display = (
        'student',
        'bonus'
    )


admin.site.register(Balance, BalanceAdmin)
