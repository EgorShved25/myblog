from django.urls import path

from . import views

from .views import subscribe, subscribe_success, search_posts



urlpatterns = [path('', views.PostView.as_view()),
               path('<int:pk>/', views.PostDetail.as_view(), name='post_detail'),
               path('review/<int:pk>/', views.AddComments.as_view(), name='add_comments'),
               path('<int:pk>/add_likes/', views.AddLike.as_view(), name='add_likes'),
               path('<int:pk>/del_likes/', views.DelLike.as_view(), name='del_likes'),
               path('about/', views.about, name='about'),
               path('subscribe/', subscribe, name='subscribe'),
               path('subscribe/success/', subscribe_success, name='subscribe_success'),
               path('search_posts/', views.search_posts, name='search_posts'),

               ]



