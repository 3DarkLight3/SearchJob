from django.contrib import admin
from .models import StoryModel, CommentModel
# Register your models here.


class StoryAdmin(admin.ModelAdmin):
    list_display = ['headline', 'for_who', 'comments', 'user']
    list_display_links = ['user']
    list_editable = ['for_who', 'comments']
    list_filter = ['timestamp', 'comments', 'for_who']
    search_fields = ['user', 'headline', 'for_who']


class CommentAdmin(admin.ModelAdmin):
    list_display = ['story', 'user']
    list_display_links = ['user']
    list_filter = ['timestamp']
    search_fields = ['story', 'user']


admin.site.register(StoryModel, StoryAdmin)
admin.site.register(CommentModel, CommentAdmin)
