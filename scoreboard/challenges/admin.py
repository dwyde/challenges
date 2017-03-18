from django.contrib import admin

from challenges.models import AutoUser, Challenge


class CustomUserAdmin(admin.ModelAdmin):

    fields = ('user_id', 'is_superuser')

# Normal model admin
admin.site.register(AutoUser, CustomUserAdmin)
admin.site.register(Challenge)
