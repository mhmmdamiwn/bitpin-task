from django.contrib import admin
from .models import Post, Rating

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'text')
    search_fields = ('title', 'text')

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'score')
    list_filter = ('post', 'user')
    search_fields = ('post__title', 'user__username')