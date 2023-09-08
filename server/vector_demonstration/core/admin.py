from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import User


class CustomUserAdmin(UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "password",
                    "first_name",
                    "last_name",
                    "email",
                )
            },
        ),
        ("Admin Options", {"classes": ("collapse",), "fields": ("is_staff",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
    list_display = ("is_active", "email", "first_name", "last_name")
    list_display_links = (
        "is_active",
        "email",
        "first_name",
        "last_name",
    )
    search_fields = (
        "email",
        "first_name",
        "last_name",
    )
    list_filter = (
        "is_active",
        "is_staff",
        "is_superuser",
    )

    ordering = []


admin.site.register(User, CustomUserAdmin)
