from django.contrib import admin
from .models import Post, Comment


class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')

admin.site.register(Comment, CommentAdmin)

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'id', 'slug', 'author', 'publish', 'status')
    list_filter = ('status', 'created', 'publish', 'author')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    # Creates lookup widget for author, rather than dropdown menu
    raw_id_fields = ('author',)



admin.site.register(Post, PostAdmin)




