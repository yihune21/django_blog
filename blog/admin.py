from django.contrib import admin
from blog.models import Category, Comment, Post

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'post', 'created_on']
    list_filter = ['created_on']
    search_fields = ['author', 'body', 'post__title']
    date_hierarchy = 'created_on'
    ordering = ['-created_on']

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created_on', 'published']
    list_filter = ['created_on', 'published', 'categories']
    search_fields = ['title', 'body']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_on'
    ordering = ['-created_on']
    filter_horizontal = ['categories']
