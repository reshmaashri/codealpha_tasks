from django.urls import path
from . import views

urlpatterns = [
    # Feed & Discovery
    path('', views.home_view, name='home'),
    path('explore/', views.explore_view, name='explore'),

    # Authentication
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # User Profile
    path('profile/', views.profile_view, name='profile_self'),
    path('profile/edit/', views.profile_edit_view, name='profile_edit'),
    path('profile/<str:username>/', views.profile_view, name='profile_user'),
    path('profile/<str:username>/follow/', views.follow_toggle_view, name='follow_toggle'),

    # Posts
    path('post/create/', views.post_create_view, name='post_create'),
    path('post/<int:pk>/', views.post_detail_view, name='post_detail'),
    path('post/<int:pk>/edit/', views.post_edit_view, name='post_edit'),
    path('post/<int:pk>/delete/', views.post_delete_view, name='post_delete'),
    path('post/<int:pk>/like/', views.like_toggle_view, name='like_toggle'),
    path('post/<int:pk>/likes-list/', views.post_likes_modal_view, name='post_likes_modal'),

    # Comments
    path('post/<int:pk>/comment/', views.comment_create_view, name='comment_create'),
    path('comment/<int:pk>/delete/', views.comment_delete_view, name='comment_delete'),
]
