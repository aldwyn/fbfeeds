from django.contrib import admin
from login.models import Post

class PostAdmin(admin.ModelAdmin):
	fieldsets = [
		('Author', {'fields': ['author']}),
		('Content', {'fields': ['content']}),
	]


admin.site.register(Post, PostAdmin)