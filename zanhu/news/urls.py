from django.urls import path

from zanhu.news.views import news_list_view, post_news, news_delete_view

app_name = "news"
urlpatterns = [
    path("news/", view=news_list_view, name="list"),
    path("news/post-news/", view=post_news, name="post_news"),
    path("news/delete/<str:pk>/", view=news_delete_view, name="delete_news"),
]
