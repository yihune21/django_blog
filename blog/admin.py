from django.contrib import admin
from blog.models import Category,Comment,Post

class CategortAdmin(admin.ModelAdmin):
    pass
class CommentAdmin(admin.ModelAdmin):
    pass
class PostAdmin(admin.ModelAdmin):
    pass

admin.site.register(Category , CategortAdmin)
admin.site.register(Comment  , CommentAdmin)
admin.site.register(Post , PostAdmin)
