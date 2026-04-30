from django.shortcuts import render, HttpResponse
from .models import Post

# Create your views here.


def home(request):
    return render(request, "home.html")


def post(request):
    posts = Post.objects.all()

    context = {
        "posts": posts
    }
    return render(request, "post.html", context)
