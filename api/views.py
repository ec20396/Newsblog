from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views import View
from django.http import (
    HttpResponse,
    HttpRequest,
    JsonResponse,
    HttpResponseRedirect,
    Http404,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django import forms
from .models import Article, Comment, CreateUser
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework.response import Response
from rest_framework import status

from api.serializers import CommentSerializer, UserLoginSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate


from django.views import View
from django.http import JsonResponse
from django.core.files.storage import default_storage


from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        user_data = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "date_of_birth": user.date_of_birth.strftime("%Y-%m-%d")
            if user.date_of_birth
            else None,
            "profile_image": request.build_absolute_uri(user.profile_image.url)
            if user.profile_image
            else None,
            "favorite_category": user.favorite_category,
        }
        return Response(user_data, status=status.HTTP_200_OK)

    def post(self, request):
        user = request.user
        print("user", request.FILES)
        date_of_birth = request.POST.get("date_of_birth")
        email = request.POST.get("email")
        profile_image = request.FILES.get("profile_image")
        print("profile_image", profile_image)
        favorite_category = request.POST.get("favorite_category")

        # Update user fields
        if date_of_birth:
            user.date_of_birth = date_of_birth
        if email:
            user.email = email
        if favorite_category:
            user.favorite_category = favorite_category
        if profile_image:
            # Save the profile image file
            file_path = default_storage.save(profile_image.name, profile_image)
            user.profile_image = file_path
        user.save()

        return JsonResponse({"success": True})


def article_to_dict(article):
    return {
        "id": article.id,
        "title": article.title,
        "content": article.content,
        "category": article.category,
        "created_at": article.created_at.strftime(
            "%Y-%m-%d %H:%M:%S"
        ),  # format datetime
    }


class ArticleCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        title = request.POST.get("title")
        content = request.POST.get("content")
        category = request.POST.get("category")
        user = request.user

        article = Article(
            title=title,
            content=content,
            category=category,
            user=user,
        )
        article.save()
        return Response(article_to_dict(article), status=status.HTTP_200_OK)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]


class ArticleListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        articles = Article.objects.filter(user=user)
        data = [self.article_to_dict(article) for article in articles]
        return JsonResponse(data, safe=False)

    @staticmethod
    def article_to_dict(article):
        return {
            "id": article.id,
            "title": article.title,
            "content": article.content,
            "category": article.category,
            "created_at": article.created_at.strftime(
                "%Y-%m-%d %H:%M:%S"
            ),  # format datetime
        }


class ALlArticleListView(APIView):
    def get(self, request):
        articles = Article.objects.all()
        data = [self.article_to_dict(article) for article in articles]
        return JsonResponse(data, safe=False)

    @staticmethod
    def article_to_dict(article):
        return {
            "id": article.id,
            "title": article.title,
            "content": article.content,
            "category": article.category,
            "created_at": article.created_at.strftime(
                "%Y-%m-%d %H:%M:%S"
            ),  # format datetime
        }


class ArticleDetailView(View):
    def get(self, request, pk):
        try:
            article = Article.objects.get(pk=pk)
        except Article.DoesNotExist:
            raise Http404("Article does not exist")

        comments = Comment.objects.filter(article=article, parent_comment=None)
        article_data = self.article_to_dict(article)
        comments_data = [
            self.comment_with_replies_to_dict(comment) for comment in comments
        ]

        return JsonResponse(
            {"article": article_data, "comments": comments_data}, safe=False
        )

    @staticmethod
    def comment_with_replies_to_dict(comment):
        comment_data = {
            "id": comment.id,
            "user": comment.user.username,
            "content": comment.content,
            "created_at": comment.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "replies": [
                ArticleDetailView.comment_with_replies_to_dict(reply)
                for reply in comment.replies.all()
            ],
        }
        return comment_data

    @staticmethod
    def article_to_dict(article):
        return {
            "id": article.id,
            "title": article.title,
            "content": article.content,
            "category": article.category,
            "created_at": article.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        }


class CommentCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        parent_comment_id = request.data.get("parent_comment")
        content = request.data.get("content")
        article_id = request.data.get("article")
        user = request.user

        comment = Comment(
            user=user,
            content=content,
            article_id=article_id,
            parent_comment_id=parent_comment_id,
        )
        comment.save()

        return Response(CommentSerializer(comment).data, status=status.HTTP_200_OK)


class CommentUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        parent_comment_id = request.data.get("parent_comment")
        content = request.data.get("content")
        article_id = request.data.get("article")
        user = request.user

        comment = Comment(
            user=user,
            content=content,
            article_id=article_id,
            parent_comment_id=parent_comment_id,
        )
        comment.save()

        return Response(CommentSerializer(comment).data, status=status.HTTP_200_OK)


class CommentUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        comment = Comment.objects.get(pk=pk)
        comment.content = request.data.get("content")
        comment.save()

        return Response(CommentSerializer(comment).data, status=status.HTTP_200_OK)


class CommentDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        comment = Comment.objects.get(pk=pk)
        comment.delete()
        return JsonResponse({"success": True})


class RegisterView(View):
    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")

        if not (username and password and email):
            return JsonResponse(
                {"success": False, "error": "All fields are required"}, status=400
            )
        if CreateUser.objects.filter(username__iexact=username).exists():
            return JsonResponse(
                {"success": False, "error": "User with this username already exists"},
                status=400,
            )
        user, created = CreateUser.objects.get_or_create(username=username, email=email)
        if created:
            user.set_password(password)
            user.save()
            return JsonResponse({"success": True})
        else:
            return JsonResponse(
                {
                    "success": False,
                    "error": "User with this username or email already exists",
                },
                status=400,
            )


class LoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data["username"]
            password = serializer.validated_data["password"]
            user = authenticate(username=username, password=password)
            if user:
                refresh = RefreshToken.for_user(user)
                return Response({"access_token": str(refresh.access_token)})
            else:
                return Response(
                    {"error": "Invalid credentials"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return JsonResponse({"success": True})
