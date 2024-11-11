from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Ticket, Comment

admin.site.register(User, UserAdmin)
admin.site.register(Ticket)
admin.site.register(Comment)