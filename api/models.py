# models.py
from django.db import models
from django.contrib.auth.models import AbstractUser


class CreateUser(AbstractUser):
    profile_image = models.ImageField(
        upload_to="profile_images/", null=True, blank=True
    )
    date_of_birth = models.DateField(null=True, blank=True)
    favorite_category = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.username


class Article(models.Model):
    title = models.CharField(max_length=255)
    user = models.ForeignKey(CreateUser, on_delete=models.CASCADE)
    content = models.TextField()
    category = models.CharField(
        max_length=255
    )  # Directly include the category field in the Article model
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    user = models.ForeignKey(CreateUser, on_delete=models.CASCADE)
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name="comments"
    )
    parent_comment = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="replies"
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id} - {self.user.username} - {self.article.title}"
