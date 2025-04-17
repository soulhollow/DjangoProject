# core/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Tag

admin.site.register(User, UserAdmin)
admin.site.register(Tag)

# contacts/admin.py
from django.contrib import admin
from .models import Contact, Policy

class PolicyInline(admin.TabularInline):
    model = Policy
    extra = 0

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'contact_type', 'user', 'lead_score')
    list_filter = ('contact_type', 'user')
    search_fields = ('first_name', 'last_name', 'email')
    inlines = [PolicyInline]

admin.site.register(Policy)

# teams/admin.py
from django.contrib import admin
from .models import TeamMember

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('upline', 'downline', 'level')
    list_filter = ('level',)