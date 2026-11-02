from django.contrib import admin
from .models import UserProfile, Post, Comment, Like, Follow


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'location', 'website', 'created_at')
    search_fields = ('user__username', 'user__email', 'bio', 'location')
    list_filter = ('created_at',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'caption_preview', 'created_at', 'likes_count', 'comments_count')
    list_filter = ('created_at',)
    search_fields = ('author__username', 'caption')

    def caption_preview(self, obj):
        return (obj.caption[:50] + '...') if len(obj.caption) > 50 else obj.caption
    caption_preview.short_description = "Caption"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'post', 'created_at', 'text_preview')
    list_filter = ('created_at',)
    search_fields = ('author__username', 'text')

    def text_preview(self, obj):
        return (obj.text[:50] + '...') if len(obj.text) > 50 else obj.text
    text_preview.short_description = "Comment"


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'post', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username',)


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('id', 'follower', 'following', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('follower__username', 'following__username')
