from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from Users.models import User
from .models import Post
from .forms import CreatePost


# SECCION DE BLOG
@login_required
def get_blog_posts(request):
    """
    Retorna todos los posts, con paginacion, para la seccion de blog
    """
    post_list = Post.objects.exclude(status=0)
    page = request.GET.get('page', 1)

    paginator = Paginator(post_list, 10)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    
    print(posts.has_other_pages)
    return render(request, 'oikos/blog.html', { 'posts': posts, 'fino': "fino" })

@login_required
def get_blog_post(request, pk):
    """
    Retorna la vista completa del post seleccionado
    """
    return render(request, 'oikos/blog.html', {'post' : Post.objects.get(pk=pk)})


# SECCION DE GESTION DE POSTS
@login_required
def get_post_user(request, user_pk):
    user = User.objects.get(pk=user_pk)
    posts = user.blog_posts.all()
    return render(request, 'blog/post.html', {'posts' : posts})

@login_required
def create_post(request):
    if request.method == "POST":
        form = CreatePost(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            messages.success(request, "Post Agregado Satisfactoriamente.")
            return redirect('blog:get_post_user', request.user.pk)
        messages.error(request, "No se ha podido agregar el Post.")
        return redirect('blog:get_post_user', request.user.pk)
    form = CreatePost()
    return render(request, "blog/addpost.html", {'form':form})

@login_required
def modify_post(request, pk):
    if request.method == "POST":
        instance = get_object_or_404(Post, pk=pk)
        form = CreatePost(request.POST, instance=instance)
        print(form)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            messages.success(request, "Post Agregado Satisfactoriamente.")
            return redirect('blog:get_post_user', request.user.pk)
        print(form.errors)
        messages.error(request, "No se ha podido agregar el Post.")
        return redirect('blog:get_post_user', request.user.pk)
    p = Post.objects.get(pk=pk)
    form = CreatePost(instance=p)
    return render(request, "blog/addpost.html", {'form':form})

@login_required
def delete_post(request):
    pk = request.POST.get("post")
    post = Post.objects.get(pk=pk)
    post.delete()
    messages.success(request,"Post Eliminado Exitosamente")
    return redirect('blog:get_post_user', request.user.pk)