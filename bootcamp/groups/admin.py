from django.contrib import admin
from bootcamp.groups.models import Group

@admin.register(Group)
class Groupdmin(admin.ModelAdmin):
    list_display = ('title', 'created', 'updated')
    date_hierarchy = 'created'
