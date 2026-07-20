from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, CodingChallenge, SelectedChallenge


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'completed', 'is_staff')
    list_filter = ('is_staff', 'completed')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Status', {'fields': ('completed', 'is_active', 'is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions')


@admin.register(CodingChallenge)
class CodingChallengeAdmin(admin.ModelAdmin):
    list_display = ('order', 'id')
    ordering = ('order',)


@admin.register(SelectedChallenge)
class SelectedChallengeAdmin(admin.ModelAdmin):
    list_display = ('applicant', 'challenge', 'passed')
    list_filter = ('passed',)
