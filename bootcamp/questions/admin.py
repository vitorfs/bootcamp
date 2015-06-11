from django.contrib import admin
from models import Question, Answer

class QuestionAdmin(admin.ModelAdmin):
    raw_id_fields = ("user",)
    list_display = ('user', 'title', 'create_date',)
    list_display_links = ('title',)
    readonly_fields = ('user',)
    def get_queryset(self, request):
        return super(QuestionAdmin, self).queryset(request).select_related('user')

class AnswerAdmin(admin.ModelAdmin):
    raw_id_fields = ("user", "question")
    list_display = ('user', 'question', 'description',)
    list_display_links = ('description',)
    readonly_fields = ('user', 'question',)

admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
