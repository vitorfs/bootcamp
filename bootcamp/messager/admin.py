from django.contrib import admin
from bootcamp.messager.models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("sender", "recipient", "timestamp")
    list_filter = ("sender", "recipient")
