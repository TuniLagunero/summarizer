from django.urls import path
from summarizer.views import index, create_post, view_post, user_login, user_logout, register, delete_post
from django.contrib import admin

urlpatterns = [
    path('', index, name='index'),
    path('create/', create_post, name='create_post'),
    path('post/<int:post_id>/', view_post, name='view_post'),
    path('login/', user_login, name='login'),
    path('register/', register, name='register'),
    path('post/<int:post_id>/delete/', delete_post, name='delete_post'),
    path('admin/', admin.site.urls),
    path('logout/', user_logout, name='user_logout'),
]