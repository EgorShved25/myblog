from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import View
from .models import Post, Likes, Subscriber
from .form import CommentsForm, SubscriberForm
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q


class PostView(View):
    '''вывод записей '''

    def get(self, request):
        posts = Post.objects.all()
        paginator = Paginator(posts, 3)
        page_number = request.GET.get('page', 1)
        page = paginator.get_page(page_number)
        return render(request, 'blog/blog.html', {'post_list': page})


def about(request):
    return render(request, 'blog/about.html')


class PostDetail(View):
    '''отдельная страница записи'''

    def get(self, request, pk):
        post = Post.objects.get(id=pk)
        return render(request, 'blog/blog_detail.html', {'post': post})


class AddComments(View):
    '''добавление комментариев'''

    def post(self, request, pk):
        form = CommentsForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.post_id = pk
            form.save()
        return redirect(f'/{pk}')


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class AddLike(View):
    def get(self, request, pk):
        ip_client = get_client_ip(request)
        try:
            Likes.objects.get(ip=ip_client, pos_id=pk)
            return redirect(f'/{pk}')
        except:
            new_like = Likes()
            new_like.ip = ip_client
            new_like.pos_id = int(pk)
            new_like.save()
            return redirect(f'/{pk}')


class DelLike(View):
    def get(self, request, pk):
        ip_client = get_client_ip(request)
        try:
            lik = Likes.objects.get(ip=ip_client)
            lik.delete()
            return redirect(f'/{pk}')
        except:
            return redirect(f'/{pk}')


def subscribe(request):
    if request.method == 'POST':
        form = SubscriberForm(request.POST)
        if form.is_valid():
            form.save()  # Сохраняем адрес электронной почты
            # Отправляем уведомление о подписке
            send_mail(
                'Подписка на обновления',
                'Спасибо за подписку на новые обновления в нашем блоге!',
                settings.DEFAULT_FROM_EMAIL,
                [form.cleaned_data['email']],
                fail_silently=False,
            )
            return redirect('subscribe_success')  # Успешный редирект
    else:
        form = SubscriberForm()

    return render(request, 'blog/subscribe.html', {'form': form})


def subscribe_success(request):
    count = Subscriber.objects.count()
    return render(request, 'blog/subscribe_success.html', {'subscriber_count': count})


def search_posts(request):
    query = request.GET.get('q')  # Получаем строку поиска из GET-запроса
    results = []  # Инициализируем results как пустой список по умолчанию
    if query:
        # Фильтруем посты по заголовку и описанию
        results = Post.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
    # Возвращаем HttpResponse даже если нет результатов
    return render(request, 'blog/search_results.html', {'results': results, 'query': query})
