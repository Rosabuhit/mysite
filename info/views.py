from django.shortcuts import render
from info.models import News

def news(request):
    posts = News.objects.all()
    return render(request, 'home.html', {'posts': posts})
