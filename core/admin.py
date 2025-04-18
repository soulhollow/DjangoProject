# core/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Tag, Task

admin.site.register(User, UserAdmin)
admin.site.register(Tag)
admin.site.register(Task)