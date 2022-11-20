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
    fields = ['name', 'team', 'colleagues']

    def colleagues_names(self, obj):
        colleagues_names = list(map(lambda loan_type: str(loan_type), obj.colleagues.all()))

        return format_html(', '.join(colleagues_names))
    colleagues_names.verbose = 'xxx'
    colleagues_names.short_description = 'colleagues'


@admin.register(SecretSanta)
class SecretSantaAdmin(admin.ModelAdmin):
    model = SecretSanta
    list_display = ['santa', 'recipient']
    fields = ['santa', 'recipient']


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
