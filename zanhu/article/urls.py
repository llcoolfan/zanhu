from django.urls import path

from article.views import article_list_view, article_create_view, draft_list_view

app_name = "articles"
urlpatterns = [
    path("", view=article_list_view, name="list"),
    path("create_article/", view=article_create_view, name="write_new"),
    path("drafts/", view=draft_list_view, name="drafts"),
]
