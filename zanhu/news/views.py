from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView, DeleteView
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseBadRequest
from django.urls import reverse_lazy
from zanhu.news.models import News
from zanhu.helpers import ajax_required, AuthorRequiredMixin


class NewListView(LoginRequiredMixin, ListView):
    model = News
    paginate_by = 20  # url中的page参数
    # context_object_name = "news_list"
    # page_kwarg = 'P' #分页的关键字
    # ordering = "-create_at"
    template_name = "news/news_list.html"  # 默认为模型类名_list.html

    def get_queryset(self):
        return News.objects.filter(reply=False)


news_list_view = NewListView.as_view()


class NewsDeletView(LoginRequiredMixin, AuthorRequiredMixin, DeleteView):
    model = News
    template_name = "news/news_confirm_delete.html"
    success_url = reverse_lazy("news:list")  # 在项目URLconf未加载时使用


news_delete_view = NewsDeletView.as_view()


@login_required
@ajax_required
@require_http_methods(['POST'])
def post_news(request):
    """发送动态，AJAX请求"""
    post = request.POST["post"].strip()  # 不要写成大写POST
    if post:
        posted = News.objects.create(user=request.user, content=post)
        html = render_to_string("news/news_single.html", {"news": posted, "request": request})
        return HttpResponse(html)
    return HttpResponseBadRequest("内容不能为空")
