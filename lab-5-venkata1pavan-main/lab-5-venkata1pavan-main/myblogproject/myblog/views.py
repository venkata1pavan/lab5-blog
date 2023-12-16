from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Avg
from .models import BlogPost, Comment, Rating
from django.contrib.auth.models import User
from .forms import BlogPostForm, CommentForm, RatingForm, UserRegistrationForm, UserLoginForm
def index(request):
    posts = BlogPost.objects.all()
    return render(request, 'myblog/index.html', {'posts': posts})

def post_detail(request, post_id):
    post = get_object_or_404(BlogPost, pk=post_id)
    comments = Comment.objects.filter(post=post)
    average_rating = Rating.objects.filter(post=post).aggregate(Avg('rating'))['rating__avg']
    return render(request, 'myblog/post_detail.html', {'post': post, 'comments': comments, 'average_rating': average_rating})

@login_required
def create_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', post_id=post.id)
    else:
        form = BlogPostForm()
    return render(request, 'myblog/create_post.html', {'form': form})

@login_required
def update_post(request, post_id):
    post = get_object_or_404(BlogPost, pk=post_id, author=request.user)
    if request.method == 'POST':
        form = BlogPostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', post_id=post.id)
    else:
        form = BlogPostForm(instance=post)
    return render(request, 'myblog/update_post.html', {'form': form, 'post': post})

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(BlogPost, pk=post_id, author=request.user)
    if request.method == 'POST':
        post.delete()
        return redirect('index')
    return render(request, 'myblog/delete_post.html', {'post': post})

def search_posts(request):
    query = request.GET.get('q')
    if query:
        posts = BlogPost.objects.filter(title__icontains=query) | BlogPost.objects.filter(content__icontains=query)
    else:
        posts = BlogPost.objects.all()
    return render(request, 'myblog/search_posts.html', {'posts': posts, 'query': query})

@login_required
def user_profile(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    posts = BlogPost.objects.filter(author=request.user)
    return render(request, 'myblog/user_profile.html', {'user_profile': user_profile, 'posts': posts})

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(BlogPost, pk=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
    return redirect('post_detail', post_id=post.id)

@login_required
def rate_post(request, post_id):
    post = get_object_or_404(BlogPost, pk=post_id)
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.user = request.user
            rating.post = post
            rating.save()
    return redirect('post_detail', post_id=post.id)

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # You can perform additional actions after registration if needed
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'myblog/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            # Authenticate user and log in
            # You may use Django's built-in authentication views here
            return redirect('index')
    else:
        form = UserLoginForm()
    return render(request, 'myblog/login.html', {'form': form})

@login_required
def user_logout(request):
    # Log out the user
    # You may use Django's built-in authentication views here
    return redirect('index')
