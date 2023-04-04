from django.contrib import admin
from content.models import *
from .models import *

# Register your models here.
admin.site.register(Category)

@admin.register(ContentLikes)
class ContentLikesAdmin(admin.ModelAdmin):
    list_display = ["user","content","likes","date"]
    search_fields = ["content__category__name"]

@admin.register(ContentComments)
class ContentCommentsAdmin(admin.ModelAdmin):
    list_display = ["user","content","comment","date"]
    search_fields = ["content__category__name"]

@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ["title","price","is_locked","home","date"]
    search_fields = ["category__name","title"]
    list_editable = ["is_locked","home","price"]
    