from django.contrib import admin
from django.contrib.auth.hashers import make_password

from users.models import User


class PasswordUserAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.password = make_password(obj.password)
        obj.user = request.user
        obj.save()


admin.site.register(User, PasswordUserAdmin)
