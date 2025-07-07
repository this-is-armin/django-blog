from django.contrib import admin
from django.utils.translation import ngettext
from django.contrib import messages

from .models import Category, Post, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'name', 'published_posts_count', 'created_at', 'updated_at']
    list_filter = ['user', 'name', 'created_at']
    list_max_show_all = 200
    list_per_page = 20
    search_fields = ['name', 'slug']
    readonly_fields = ['created_at', 'updated_at']
    prepopulated_fields = {'slug': ['name']}


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'category', 'title', 'is_published', 'created_at', 'updated_at']
    list_filter = ['user', 'category', 'is_published', 'created_at']
    list_max_show_all = 200
    list_per_page = 20
    search_fields = ['title', 'description']
    readonly_fields = ['created_at', 'updated_at']
    prepopulated_fields = {'slug': ['title']}
    actions = ['publish', 'unpublish']

    def publish(self, request, queryset):
        """To publish selected posts"""

        updated = queryset.update(is_published=True)
        self.message_user(
            request,
            ngettext(
                f"Successfully published {updated} post.",
                f"Successfully published {updated} posts.",
                updated
            ),
            messages.SUCCESS
        )
    publish.short_description = 'Publish selected posts'


    def unpublish(self, request, queryset):
        """To unpublish selected posts"""

        updated = queryset.update(is_published=False)
        self.message_user(
            request,
            ngettext(
                f"Successfully unpublished {updated} post.",
                f"Successfully unpublished {updated} posts.",
                updated
            ),
            messages.SUCCESS
        )
    unpublish.short_description = 'Unpublish selected posts'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'post', 'user', 'is_published', 'created_at', 'updated_at']
    list_filter = ['post', 'is_published', 'created_at']
    list_max_show_all = 200
    list_per_page = 20
    search_fields = ['body']
    readonly_fields = ['created_at', 'updated_at']
    actions = ['publish', 'unpublish']

    def publish(self, request, queryset):
        """To publish selected comments"""

        updated = queryset.update(is_published=True)
        self.message_user(
            request,
            ngettext(
                f"Successfully published {updated} comment.",
                f"Successfully published {updated} comments.",
                updated
            ),
            messages.SUCCESS
        )
    publish.short_description = 'Publish selected comments'


    def unpublish(self, request, queryset):
        """To unpublish selected comments"""

        updated = queryset.update(is_published=False)
        self.message_user(
            request,
            ngettext(
                f"Successfully unpublished {updated} comment.",
                f"Successfully unpublished {updated} comments.",
                updated
            ),
            messages.SUCCESS
        )
    unpublish.short_description = 'Unpublish selected comments'