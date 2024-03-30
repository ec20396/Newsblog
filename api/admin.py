from django.contrib import admin
from .models import CreateUser, Article, Comment

# Register your models here.
admin.site.register(CreateUser)
admin.site.register(Article)
admin.site.register(Comment)
