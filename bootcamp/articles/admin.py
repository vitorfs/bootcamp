from django.contrib import admin
from models import Article, ArticleComment

class ArticleAdmin(admin.ModelAdmin):
    raw_id_fields = ("create_user", "update_user",)
    list_display = ('create_user', 'update_user', 'title', 'slug', 'status',)
    list_display_links = ('title',)
    list_filter = ('status',)
    search_fields = ('title',)

class ArticleCommentAdmin(admin.ModelAdmin):
    raw_id_fields = ("article", "user",)
    list_display = ('user', 'article', 'comment',)
    list_display_links = ('comment',)
    readonly_fields = ('article', 'user',)
    search_fields = ('comment',)

admin.site.register(Article, ArticleAdmin)
admin.site.register(ArticleComment, ArticleCommentAdmin)
