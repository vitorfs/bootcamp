from django.contrib import admin
from models import Feed

class FeedAdmin(admin.ModelAdmin):
    raw_id_fields = ("user", "parent",)
    list_display = ('user', 'parent', 'post', 'likes',)
    list_display_links = ('post',)
    readonly_fields = ('parent',)
    search_fields = ('post',)

admin.site.register(Feed, FeedAdmin)
