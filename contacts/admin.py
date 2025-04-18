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