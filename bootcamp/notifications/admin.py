from django.contrib import admin
from bootcamp.notifications.models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    raw_id_fields = ('recipient', )
    list_display = ('recipient', 'actor', 'target', 'verb', 'unread',)
    list_filter = ('unread', )
