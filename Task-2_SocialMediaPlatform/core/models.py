import re
from urllib.parse import quote
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.safestring import mark_safe


class UserProfile(models.Model):
    """
    Extends the built-in Django User model with profile data including
    avatar, bio, location, website, and social metrics.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True, help_text="Short biography or intro")
    location = models.CharField(max_length=100, blank=True, help_text="City, Country")
    website = models.URLField(max_length=200, blank=True, help_text="Personal or portfolio link")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def get_avatar_url(self):
        """
        Returns uploaded avatar URL if present, or an inline SVG avatar
        with user initials and a vibrant gradient background.
        """
        if self.avatar and hasattr(self.avatar, 'url'):
            return self.avatar.url

        # Fallback to generated initials SVG
        name = self.user.get_full_name() or self.user.username
        initials = "".join([part[0] for part in name.split()[:2]]).upper() or self.user.username[:2].upper()
        
        # Color palette hashing based on username
        colors = [
            ("#4F46E5", "#7C3AED"),
            ("#2563EB", "#38BDF8"),
            ("#7C3AED", "#EC4899"),
            ("#059669", "#10B981"),
            ("#D97706", "#F59E0B"),
            ("#DC2626", "#F43F5E"),
        ]
        color_idx = sum(ord(c) for c in self.user.username) % len(colors)
        c1, c2 = colors[color_idx]

        svg = (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100" viewBox="0 0 100 100">'
            f'<defs><linearGradient id="g" x1="0%" y1="0%" x2="100%" y2="100%">'
            f'<stop offset="0%" stop-color="{c1}"/>'
            f'<stop offset="100%" stop-color="{c2}"/>'
            f'</linearGradient></defs>'
            f'<circle cx="50" cy="50" r="50" fill="url(#g)"/>'
            f'<text x="50" y="58" font-family="Segoe UI, -apple-system, sans-serif" font-size="34" '
            f'font-weight="bold" fill="#ffffff" text-anchor="middle">{initials}</text>'
            f'</svg>'
        )
        return f"data:image/svg+xml;utf8,{quote(svg)}"

    @property
    def display_name(self):
        full = self.user.get_full_name()
        return full.strip() if full.strip() else self.user.username

    def followers_count(self):
        return self.user.follower_relations.count()

    def following_count(self):
        return self.user.following_relations.count()

    def posts_count(self):
        return self.user.posts.count()

    def likes_received_count(self):
        return sum(post.likes.count() for post in self.user.posts.all())

    def is_followed_by(self, user):
        if not user or not user.is_authenticated:
            return False
        return self.user.follower_relations.filter(follower=user).exists()


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """Automatically create the user profile when a User is created."""
    if created:
        UserProfile.objects.get_or_create(user=instance)



class Post(models.Model):
    """
    Social media post model with image, caption, author, and timestamps.
    """
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    image = models.ImageField(upload_to='posts/', blank=False, null=False, help_text="Upload post photo")
    caption = models.TextField(max_length=2200, blank=True, help_text="Write a caption...")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Post by @{self.author.username} at {self.created_at.strftime('%Y-%m-%d %H:%M')}"

    def likes_count(self):
        return self.likes.count()

    def comments_count(self):
        return self.comments.count()

    def is_liked_by(self, user):
        if not user or not user.is_authenticated:
            return False
        return self.likes.filter(user=user).exists()

    def get_caption_with_hashtags(self):
        """Highlights hashtags in caption with styled spans."""
        if not self.caption:
            return ""
        # Match #hashtag
        escaped = self.caption
        formatted = re.sub(
            r'(#\w+)',
            r'<span class="hashtag font-medium text-primary hover:underline">\1</span>',
            escaped
        )
        return mark_safe(formatted)


class Comment(models.Model):
    """
    Comment on a post.
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Comment by @{self.author.username} on post {self.post_id}"


class Like(models.Model):
    """
    Like on a post, constrained to prevent duplicate likes from the same user.
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'user')
        ordering = ['-created_at']

    def __str__(self):
        return f"@{self.user.username} likes post {self.post_id}"


class Follow(models.Model):
    """
    Follower / Following relationship between users.
    """
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following_relations')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower_relations')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')
        ordering = ['-created_at']

    def __str__(self):
        return f"@{self.follower.username} follows @{self.following.username}"
