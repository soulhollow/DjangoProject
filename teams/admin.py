# teams/admin.py
from django.contrib import admin
from .models import TeamMember

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('upline', 'downline', 'level')
    list_filter = ('level',)