from django.shortcuts import render
from info.models import News, ContactForm
from django.utils import timezone
from django.views.generic import TemplateView, View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail, BadHeaderError


def contactView(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        # Если форма заполнена корректно, сохраняем все введённые пользователем значения
        if form.is_valid():
            subject = form.cleaned_data['subject']
            sender = form.cleaned_data['sender']
            message = form.cleaned_data['message']
            copy = form.cleaned_data['copy']

            recipients = ['ВАШ_EMAIL_ДЛЯ_ПОЛУЧЕНИЯ_СООБЩЕНИЯ']
            # Если пользователь захотел получить копию себе, добавляем его в список получателей
            if copy:
                recipients.append(sender)
            try:
                send_mail(subject, message, 'ВАШ_EMAIL_ДЛЯ_ОТПРАВКИ_СООБЩЕНИЯ', recipients)
            except BadHeaderError:  # Защита от уязвимости
                return HttpResponse('Invalid header found')
            # Переходим на другую страницу, если сообщение отправлено
            return render(request, 'thanks.html')
    else:
        # Заполняем форму
        form = ContactForm()
    # Отправляем форму на страницу
    return render(request, 'contact.html', {'form': form})


class PageView(TemplateView):
    template_name = "home.html"

class NewsView(View):

    def get(self, request):
        news = News.objects.filter(created_date__lte=timezone.now()).order_by('-created_date')
        last_news = None

        if len(news) > 0:
            last_news = news[0]
            if len(news) >= 5:
                paginator = Paginator(news, 5)
            else:
                paginator = Paginator(news, len(news))
            page = request.GET.get('page')
            try:
                news = paginator.page(page)
            except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                news = paginator.page(1)
            except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
                news = paginator.page(paginator.num_pages)
        return render(request, 'news.html', {'news': news, "last_news": last_news})