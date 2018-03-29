from django.contrib import admin
from bootcamp.notifications.models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'actor', 'verb', 'unread', )
    list_filter = ('recipient', 'unread', )
