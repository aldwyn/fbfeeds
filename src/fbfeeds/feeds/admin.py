from django.contrib import admin
from feeds.models import Post, Like, Comment, Profile


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 3


class PostAdmin(admin.ModelAdmin):
    fields = ['author', 'content']
    list_display = ('content', 'author', 'post_date')
    search_fields = ['content', 'author']
    inlines = [CommentInline]


admin.site.register(Post, PostAdmin)
admin.site.register(Like)
admin.site.register(Profile)
