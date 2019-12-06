from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    path('', views.get_blog_posts, name='blog'), 
    path('<int:pk>/', views.get_blog_post, name='get_blog_post'),
    path('post/<int:user_pk>/', views.get_post_user, name='get_post_user'),
    path('post/add/', views.create_post, name='create_post'),
    path('post/modify/<int:pk>', views.modify_post, name='modify_post'),
    path('post/delete/', views.delete_post, name='delete_post'),
    
]
