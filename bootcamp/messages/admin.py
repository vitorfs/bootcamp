from django.contrib import admin
from models import Message

class MessageAdmin(admin.ModelAdmin):
    raw_id_fields = ("user", "conversation", "from_user",)
    list_display = ('from_user', 'user', 'message', 'is_read',)
    list_display_links = ('message',)
    list_filter = ('is_read',)
    readonly_fields = ('user', 'conversation', 'from_user',)

admin.site.register(Message, MessageAdmin)
