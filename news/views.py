from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from .models import News
from .forms import NewsForm
from django.core.paginator import Paginator


def news_list(request):
    news = News.objects.filter(is_announcement=False)
    announcements = News.objects.filter(is_announcement=True)

    news_paginator = Paginator(news, 4)
    announcement_paginator = Paginator(announcements, 4)

    news_page_number = request.GET.get('news_page', 1)
    announcement_page_number = request.GET.get('announcement_page', 1)

    news_page_obj = news_paginator.get_page(news_page_number)
    announcement_page_obj = announcement_paginator.get_page(announcement_page_number)

    return render(request, 'news/news_list.html', {
        'news_page_obj': news_page_obj,
        'announcement_page_obj': announcement_page_obj
    })


def news_detail(request, type, pk):
    if type == 'news':
        news = get_object_or_404(News, pk=pk, is_announcement=False)
    elif type == 'announcement':
        news = get_object_or_404(News, pk=pk, is_announcement=True)
    else:
        raise Http404("Invalid news type")
    return render(request, 'news/news_detail.html', {'news': news})


def news_create(request):
    if request.method == 'POST':
        form = NewsForm(request.POST)
        if form.is_valid():
            news = form.save(commit=False)
            news.author = request.user
            news.save()
            return redirect('news_list')
    else:
        form = NewsForm()
    return render(request, 'news/news_form.html', {'form': form, 'news': None})

def news_edit(request, pk):
    news = get_object_or_404(News, pk=pk)
    if request.method == 'POST':
        form = NewsForm(request.POST, instance=news)
        if form.is_valid():
            form.save()
            return redirect('news_list')
    else:
        form = NewsForm(instance=news)
    return render(request, 'news/news_form.html', {'form': form, 'news': news})



def news_delete(request, pk):
    news = get_object_or_404(News, pk=pk)
    if request.method == 'POST':
        news.delete()
        return redirect('news_list')
    return render(request, 'news/news_confirm_delete.html', {'news': news})



