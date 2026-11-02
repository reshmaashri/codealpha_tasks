import json
import re
from collections import Counter
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponseForbidden
from django.db.models import Q, Count
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator

from .models import UserProfile, Post, Comment, Like, Follow
from .forms import (
    UserRegistrationForm,
    UserLoginForm,
    PostCreateForm,
    PostEditForm,
    ProfileEditForm,
    CommentForm,
)


def get_common_context(request):
    """
    Returns suggested creators, trending hashtags, and platform community stats.
    """
    # Suggested users to follow
    suggested_users = []
    if request.user.is_authenticated:
        following_ids = request.user.following_relations.values_list('following_id', flat=True)
        suggested_users = User.objects.exclude(
            id=request.user.id
        ).exclude(
            id__in=following_ids
        ).select_related('profile').annotate(
            post_count=Count('posts')
        ).order_by('-post_count', '-date_joined')[:5]
    else:
        suggested_users = User.objects.select_related('profile').annotate(
            post_count=Count('posts')
        ).order_by('-post_count', '-date_joined')[:5]

    # Trending hashtags extracted from recent posts
    recent_captions = Post.objects.values_list('caption', flat=True)[:50]
    hashtags = []
    for cap in recent_captions:
        if cap:
            tags = re.findall(r'#(\w+)', cap)
            hashtags.extend([t.lower() for t in tags])
    trending_tags = [item[0] for item in Counter(hashtags).most_common(5)]
    if not trending_tags:
        trending_tags = ['connecthub', 'technology', 'design', 'lifestyle', 'creators']

    stats = {
        'total_posts': Post.objects.count(),
        'total_users': User.objects.count(),
        'total_likes': Like.objects.count(),
    }

    return {
        'suggested_users': suggested_users,
        'trending_tags': trending_tags,
        'stats': stats,
    }


def home_view(request):
    """
    Main feed view. Shows posts from followed creators and own posts,
    with an instant toggle to explore all posts.
    """
    feed_type = request.GET.get('feed', 'following')
    
    # If not authenticated, direct to explore feed
    if not request.user.is_authenticated:
        feed_type = 'explore'

    # Filter posts based on feed type
    if feed_type == 'following' and request.user.is_authenticated:
        following_ids = list(request.user.following_relations.values_list('following_id', flat=True))
        # Include user's own posts and posts from followed users
        feed_user_ids = following_ids + [request.user.id]
        posts_qs = Post.objects.filter(author_id__in=feed_user_ids)
    else:
        # Explore / All posts
        feed_type = 'explore'
        posts_qs = Post.objects.all()

    # Search filtering if 'q' parameter is present
    search_query = request.GET.get('q', '').strip()
    if search_query:
        if search_query.startswith('#'):
            tag = search_query[1:]
            posts_qs = posts_qs.filter(caption__icontains=f"#{tag}")
        else:
            posts_qs = posts_qs.filter(
                Q(caption__icontains=search_query) |
                Q(author__username__icontains=search_query) |
                Q(author__first_name__icontains=search_query) |
                Q(author__last_name__icontains=search_query)
            )

    # Hashtag filtering if 'tag' is provided
    tag_filter = request.GET.get('tag', '').strip()
    if tag_filter:
        posts_qs = posts_qs.filter(caption__icontains=f"#{tag_filter}")

    posts_qs = posts_qs.select_related('author', 'author__profile').prefetch_related(
        'likes',
        'comments__author',
        'comments__author__profile'
    ).order_by('-created_at')

    # Pagination: 10 posts per page
    paginator = Paginator(posts_qs, 10)
    page_number = request.GET.get('page', 1)
    posts = paginator.get_page(page_number)

    # Pre-calculate liked status for authenticated user
    if request.user.is_authenticated:
        user_liked_post_ids = set(
            Like.objects.filter(
                user=request.user,
                post__in=posts
            ).values_list('post_id', flat=True)
        )
        for post in posts:
            post.is_liked_by_current_user = post.id in user_liked_post_ids
    else:
        for post in posts:
            post.is_liked_by_current_user = False

    post_form = PostCreateForm()
    comment_form = CommentForm()

    context = {
        'posts': posts,
        'feed_type': feed_type,
        'search_query': search_query,
        'tag_filter': tag_filter,
        'post_form': post_form,
        'comment_form': comment_form,
        'has_following': request.user.is_authenticated and request.user.following_relations.exists(),
        **get_common_context(request),
    }
    return render(request, 'core/home.html', context)


def explore_view(request):
    """
    Dedicated Explore page with grid/card views and search.
    """
    search_query = request.GET.get('q', '').strip()
    tag_filter = request.GET.get('tag', '').strip()

    posts_qs = Post.objects.all().select_related('author', 'author__profile').prefetch_related(
        'likes', 'comments'
    )

    if search_query:
        if search_query.startswith('#'):
            tag = search_query[1:]
            posts_qs = posts_qs.filter(caption__icontains=f"#{tag}")
        else:
            posts_qs = posts_qs.filter(
                Q(caption__icontains=search_query) |
                Q(author__username__icontains=search_query) |
                Q(author__first_name__icontains=search_query) |
                Q(author__last_name__icontains=search_query)
            )

    if tag_filter:
        posts_qs = posts_qs.filter(caption__icontains=f"#{tag_filter}")

    posts_qs = posts_qs.order_by('-created_at')

    # Pre-calculate liked status
    if request.user.is_authenticated:
        user_liked_post_ids = set(
            Like.objects.filter(
                user=request.user,
                post__in=posts_qs[:30]
            ).values_list('post_id', flat=True)
        )
        for post in posts_qs:
            post.is_liked_by_current_user = post.id in user_liked_post_ids
    else:
        for post in posts_qs:
            post.is_liked_by_current_user = False

    context = {
        'posts': posts_qs,
        'search_query': search_query,
        'tag_filter': tag_filter,
        **get_common_context(request),
    }
    return render(request, 'core/explore.html', context)


def register_view(request):
    """
    User registration with automatic profile creation and login.
    """
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            # Create user
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            # Update profile
            profile = getattr(user, 'profile', None) or UserProfile.objects.get(user=user)
            if form.cleaned_data.get('bio'):
                profile.bio = form.cleaned_data['bio']
            if form.cleaned_data.get('avatar'):
                profile.avatar = form.cleaned_data['avatar']
            profile.save()

            # Log user in
            login(request, user)
            messages.success(request, f"Welcome to ConnectHub, {user.first_name or user.username}! Your account has been created.")
            return redirect('home')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserRegistrationForm()

    return render(request, 'core/register.html', {'form': form})


def login_view(request):
    """
    User login supporting username or email, plus 1-click Demo Accounts.
    """
    if request.user.is_authenticated:
        return redirect('home')

    # Check for 1-click demo login request (e.g. ?demo=alex)
    demo_user_param = request.GET.get('demo')
    if demo_user_param:
        demo_user = User.objects.filter(username__iexact=demo_user_param).first()
        if demo_user:
            login(request, demo_user)
            messages.success(request, f"Logged in as demo user @{demo_user.username} ({demo_user.get_full_name() or 'Creator'})")
            return redirect('home')

    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username_or_email = form.cleaned_data['username'].strip()
            password = form.cleaned_data['password']
            remember_me = form.cleaned_data.get('remember_me', True)

            # Check if input is email
            user_obj = None
            if '@' in username_or_email:
                user_obj = User.objects.filter(email__iexact=username_or_email).first()
                if user_obj:
                    user = authenticate(request, username=user_obj.username, password=password)
                else:
                    user = None
            else:
                user = authenticate(request, username=username_or_email, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    if not remember_me:
                        request.session.set_expiry(0)  # Expires on browser close
                    messages.success(request, f"Welcome back, {user.first_name or user.username}!")
                    next_url = request.GET.get('next')
                    return redirect(next_url if next_url else 'home')
                else:
                    messages.error(request, "This account is inactive. Please contact support.")
            else:
                messages.error(request, "Invalid username/email or password. Please try again.")
    else:
        form = UserLoginForm()

    return render(request, 'core/login.html', {'form': form})


@login_required
def logout_view(request):
    """Log out user and redirect to login."""
    logout(request)
    messages.info(request, "You have been logged out of ConnectHub. See you again soon!")
    return redirect('login')


def profile_view(request, username=None):
    """
    User profile page displaying profile stats, bio, and all posts.
    """
    if not username:
        if request.user.is_authenticated:
            return redirect('profile_user', username=request.user.username)
        return redirect('login')

    target_user = get_object_or_404(User.objects.select_related('profile'), username__iexact=username)
    profile = target_user.profile

    tab = request.GET.get('tab', 'posts')
    if tab == 'likes':
        # Posts this user has liked
        liked_post_ids = Like.objects.filter(user=target_user).values_list('post_id', flat=True)
        posts = Post.objects.filter(id__in=liked_post_ids).select_related('author', 'author__profile').prefetch_related('likes', 'comments').order_by('-created_at')
    else:
        # User's own posts
        tab = 'posts'
        posts = target_user.posts.all().select_related('author', 'author__profile').prefetch_related('likes', 'comments').order_by('-created_at')

    # Pre-calculate liked status
    if request.user.is_authenticated:
        user_liked_post_ids = set(
            Like.objects.filter(
                user=request.user,
                post__in=posts
            ).values_list('post_id', flat=True)
        )
        for post in posts:
            post.is_liked_by_current_user = post.id in user_liked_post_ids
    else:
        for post in posts:
            post.is_liked_by_current_user = False

    is_following = False
    if request.user.is_authenticated and request.user != target_user:
        is_following = Follow.objects.filter(follower=request.user, following=target_user).exists()

    context = {
        'profile_user': target_user,
        'profile': profile,
        'posts': posts,
        'active_tab': tab,
        'is_following': is_following,
        'is_own_profile': request.user.is_authenticated and request.user == target_user,
        **get_common_context(request),
    }
    return render(request, 'core/profile.html', context)


@login_required
def profile_edit_view(request):
    """Edit current user's profile information and avatar."""
    profile = request.user.profile

    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            # Update User first/last name
            request.user.first_name = form.cleaned_data.get('first_name', '')
            request.user.last_name = form.cleaned_data.get('last_name', '')
            request.user.save()

            form.save()
            messages.success(request, "Your profile has been updated successfully!")
            return redirect('profile_user', username=request.user.username)
        else:
            messages.error(request, "Could not update profile. Please verify your inputs.")
    else:
        initial_data = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
        }
        form = ProfileEditForm(instance=profile, initial=initial_data)

    return render(request, 'core/profile_edit.html', {'form': form})


@login_required
def post_create_view(request):
    """
    Create a new post with image and optional caption.
    Supports both traditional POST and AJAX requests.
    """
    if request.method == 'POST':
        form = PostCreateForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()

            if request.headers.get('x-requested-with') == 'XMLHttpRequest' or 'application/json' in request.headers.get('Accept', ''):
                return JsonResponse({
                    'success': True,
                    'post_id': post.id,
                    'message': 'Post published successfully!'
                })

            messages.success(request, "Your post is now live!")
            return redirect('home')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                errors = [err for field_errors in form.errors.values() for err in field_errors]
                return JsonResponse({'success': False, 'errors': errors}, status=400)
            for error in form.errors.values():
                messages.error(request, error)
            return redirect('home')

    return redirect('home')


@login_required
def post_edit_view(request, pk):
    """Edit an existing post's caption and/or image."""
    post = get_object_or_404(Post, pk=pk)
    
    # Ownership verification
    if post.author != request.user:
        return HttpResponseForbidden("You do not have permission to edit this post.")

    if request.method == 'POST':
        form = PostEditForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            # If no new image was uploaded, preserve existing image
            if not form.cleaned_data.get('image'):
                post.caption = form.cleaned_data.get('caption', '')
                post.save()
            else:
                form.save()

            messages.success(request, "Post updated successfully!")
            return redirect('post_detail', pk=post.pk)
        else:
            messages.error(request, "Could not update post. Please check the errors.")
    else:
        form = PostEditForm(instance=post)

    return render(request, 'core/post_edit.html', {'form': form, 'post': post})


@login_required
@require_POST
def post_delete_view(request, pk):
    """Delete a post (owner only). Supports AJAX and standard POST."""
    post = get_object_or_404(Post, pk=pk)

    if post.author != request.user:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'error': 'Forbidden'}, status=403)
        return HttpResponseForbidden("You cannot delete another user's post.")

    post.delete()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'message': 'Post deleted.'})

    messages.success(request, "Post has been removed.")
    return redirect('home')


def post_detail_view(request, pk):
    """Standalone post view page with comments and full image."""
    post = get_object_or_404(
        Post.objects.select_related('author', 'author__profile').prefetch_related(
            'likes', 'comments__author', 'comments__author__profile'
        ),
        pk=pk
    )

    if request.user.is_authenticated:
        post.is_liked_by_current_user = post.is_liked_by(request.user)
    else:
        post.is_liked_by_current_user = False

    comment_form = CommentForm()

    context = {
        'post': post,
        'comment_form': comment_form,
        **get_common_context(request),
    }
    return render(request, 'core/post_detail.html', context)


@login_required
@require_POST
def like_toggle_view(request, pk):
    """
    Toggle like on a post. Returns JSON with updated count and state.
    Prevents duplicate likes with get_or_create / delete logic.
    """
    post = get_object_or_404(Post, pk=pk)
    like_obj = Like.objects.filter(post=post, user=request.user).first()

    if like_obj:
        like_obj.delete()
        liked = False
    else:
        Like.objects.create(post=post, user=request.user)
        liked = True

    total_likes = post.likes.count()

    return JsonResponse({
        'success': True,
        'liked': liked,
        'likes_count': total_likes,
    })


@login_required
@require_POST
def comment_create_view(request, pk):
    """Add a new comment to a post. Supports AJAX and standard POST."""
    post = get_object_or_404(Post, pk=pk)
    form = CommentForm(request.POST)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.author = request.user
        comment.save()

        if request.headers.get('x-requested-with') == 'XMLHttpRequest' or 'application/json' in request.headers.get('Accept', ''):
            return JsonResponse({
                'success': True,
                'comment_id': comment.id,
                'text': comment.text,
                'author_username': comment.author.username,
                'author_display_name': comment.author.profile.display_name,
                'author_avatar': comment.author.profile.get_avatar_url(),
                'created_at': "Just now",
                'comments_count': post.comments.count(),
            })

        messages.success(request, "Comment added!")
        return redirect(f"{request.META.get('HTTP_REFERER', '/')}#post-{post.id}")

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'success': False, 'errors': form.errors}, status=400)

    messages.error(request, "Could not add comment.")
    return redirect('home')


@login_required
@require_POST
def comment_delete_view(request, pk):
    """Delete a comment (comment author or post owner)."""
    comment = get_object_or_404(Comment, pk=pk)
    post = comment.post

    if comment.author != request.user and post.author != request.user:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'error': 'Forbidden'}, status=403)
        return HttpResponseForbidden("You cannot delete this comment.")

    comment.delete()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'comments_count': post.comments.count(),
        })

    messages.success(request, "Comment deleted.")
    return redirect(f"{request.META.get('HTTP_REFERER', '/')}#post-{post.id}")


@login_required
@require_POST
def follow_toggle_view(request, username):
    """
    Follow or unfollow a user.
    Prevents following self. Returns JSON with updated state and counts.
    """
    target_user = get_object_or_404(User, username__iexact=username)

    if request.user == target_user:
        return JsonResponse({
            'success': False,
            'error': "You cannot follow yourself."
        }, status=400)

    follow_relation = Follow.objects.filter(follower=request.user, following=target_user).first()

    if follow_relation:
        follow_relation.delete()
        is_following = False
    else:
        Follow.objects.create(follower=request.user, following=target_user)
        is_following = True

    return JsonResponse({
        'success': True,
        'is_following': is_following,
        'followers_count': target_user.follower_relations.count(),
        'following_count': target_user.following_relations.count(),
    })


def post_likes_modal_view(request, pk):
    """Returns JSON list of users who liked a post."""
    post = get_object_or_404(Post, pk=pk)
    likes = post.likes.select_related('user', 'user__profile')
    data = []
    for like in likes:
        data.append({
            'username': like.user.username,
            'display_name': like.user.profile.display_name,
            'avatar': like.user.profile.get_avatar_url(),
        })
    return JsonResponse({'likes': data, 'total': len(data)})
