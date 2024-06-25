from django.shortcuts import render
from django.http import HttpResponse
from .models import BlogPost

# Create your views here.
def index(request):
    myposts = BlogPost.objects.all()
    print(myposts)
    return render(request, 'blogg/index.html', {'myposts':myposts})

def bloggPost(request, id):
    post = BlogPost.objects.filter(Post_id= id).first()
    print(post)
    return render(request, 'blogg/bloggPost.html', {'post': post})