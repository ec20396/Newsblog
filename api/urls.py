"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    ALlArticleListView,
    ArticleListView,
    ArticleCreateView,
    ArticleDetailView,
    CommentCreateView,
    CommentUpdateView,
    CommentDeleteView,
    RegisterView,
    LoginView,
    LogoutView,
    ProfileView,
)

urlpatterns = [
    path("article/", ArticleListView.as_view(), name="article_list"),
    path("article/all/", ALlArticleListView.as_view(), name="all_article_list"),
    path("article/create/", ArticleCreateView.as_view(), name="article_create"),
    path("article/<int:pk>/", ArticleDetailView.as_view(), name="article_detail"),
    path("comments/create/", CommentCreateView.as_view(), name="comment_create"),
    path(
        "comments/<int:pk>/update/", CommentUpdateView.as_view(), name="comment_update"
    ),
    path(
        "comments/<int:pk>/delete/", CommentDeleteView.as_view(), name="comment_delete"
    ),
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("user/profile/", ProfileView.as_view(), name="user_profile"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
