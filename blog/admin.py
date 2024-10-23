from django.contrib import admin
from .models import Post, Comments, Subscriber


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author')  # загаловок таблицы


@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ('name', 'post')

@admin.register(Subscriber)
class Subscriber(admin.ModelAdmin):
    list_display = ('email', 'created_at')
