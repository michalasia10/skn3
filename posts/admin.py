from django.contrib import admin
from .models import Post,Gallery


# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish', 'tags', 'status',)
    list_filter = ('created', 'publish', 'author')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    ordering = ('publish',)


admin.register(PostAdmin)


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ('title', 'file')
    search_fields = ('title',)


admin.register(GalleryAdmin)
