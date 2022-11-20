from django.contrib import admin
from django.utils.html import format_html

from .models import Celebration, Member, SecretSanta, Team


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    model = Team
    list_display = ['name']
    fields = ['name']


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    model = Member
    list_display = ['name', 'team', 'colleagues_names']
    fields = ['name', 'email_address', 'team', 'colleagues']

    def colleagues_names(self, obj):
        colleagues_names = list(map(lambda loan_type: str(loan_type), obj.colleagues.all()))

        return format_html(', '.join(colleagues_names))
    colleagues_names.verbose = 'xxx'
    colleagues_names.short_description = 'colleagues'


def resend_email(modeladmin, request, queryset):
    for secret_santa in queryset:
        secret_santa.resend_email()

resend_email.short_description = "Receive a follow-up letter with the recipient of the gift"


@admin.register(SecretSanta)
class SecretSantaAdmin(admin.ModelAdmin):
    model = SecretSanta
    list_display = ['santa', 'hashed_recipient_info', 'celebration']
    fields = ['santa', 'celebration']

    def hashed_recipient_info(self, obj):
        return obj.recipient.hashed_email

    hashed_recipient_info.verbose = 'xxx'
    hashed_recipient_info.short_description = 'Hashed recipient info'

    actions = [resend_email]

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False


def create_secret_santa(modeladmin, request, queryset):
    for celebration in queryset:
        celebration.run()


create_secret_santa.short_description = "Let the celebration begin!"

@admin.register(Celebration)
class CelebrationAdmin(admin.ModelAdmin):
    model = Celebration
    list_display = ['year', 'team']
    fields = ['year', 'team']

    actions = [create_secret_santa]
