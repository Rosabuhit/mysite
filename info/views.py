from django.shortcuts import render
from info.models import News, ContactForm
from django.utils import timezone
from django.views.generic import TemplateView, ListView
from django.shortcuts import render, get_object_or_404, render_to_response
from django.http import HttpResponse
from django.core.mail import send_mail, BadHeaderError
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


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

class NewsView(ListView):
    model = News
    context_object_name = 'news'
    template_name = 'news.html'
    paginate_by = 4

    def get_queryset(self):
        qs = News.objects.filter(created_date__lte=timezone.now()).order_by('-created_date')
        return qs


def news_detail(request, pk):
    news = get_object_or_404(News, pk=pk)
    return render(request, 'news_detail.html', {'news': news})


def search(request):
    q = request.GET['q']
    res = [i for i in q.split()]
    cash = []
    result = []
    add_res = []
    if q:
        result = []
        for j in res:
            if j not in cash:
                cash.append(j)
                result.append(News.objects.filter(
                    Q(title__icontains=j) |
                    Q(body__icontains=j)))

    if len(result) > 0:
        add_res = [i for i in result[-1]]
        if len(add_res) > 1:
            add_res = add_res[-1]
        if len(result) >= 2:
            paginator = Paginator(result, 2)
        else:
            paginator = Paginator(result, len(result))
        page = request.GET.get('page')
        try:
            result = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            result = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            result = paginator.page(paginator.num_pages)
    return render_to_response('search.html',
                              {"result": result, "add_res": add_res, 'q': q})

