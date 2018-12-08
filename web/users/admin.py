from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import UserHC
# Register your models here.


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = UserHC
    list_display = ['first_name', 'last_name', 'uses_email_username', 'username', 'email', ]
    # list_display = ['username', 'email', ]


admin.site.register(UserHC, CustomUserAdmin)