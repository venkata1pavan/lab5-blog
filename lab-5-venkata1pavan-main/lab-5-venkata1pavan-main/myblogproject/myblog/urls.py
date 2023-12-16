from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Home page showing a list of blog posts
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),  # View a single blog post
    path('post/create/', views.create_post, name='create_post'),  # Create a new blog post
    path('post/<int:post_id>/update/', views.update_post, name='update_post'),  # Update an existing blog post
    path('post/<int:post_id>/delete/', views.delete_post, name='delete_post'),  # Delete an existing blog post
    path('search/', views.search_posts, name='search_posts'),  # Search for blog posts by title or content
    path('profile/', views.user_profile, name='user_profile'),  # User profile page
    path('post/<int:post_id>/comment/', views.add_comment, name='add_comment'),  # Add a comment to a blog post
    path('post/<int:post_id>/rate/', views.rate_post, name='rate_post'),  # Rate a blog post
    path('register/', views.register, name='register'),  # User registration
    path('login/', views.user_login, name='login'),  # User login
    path('logout/', views.user_logout, name='logout'),  # User logout
]
