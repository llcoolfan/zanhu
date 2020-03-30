from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView
from article.models import Articles
from article.forms import ArticleForm


class ArticleList(LoginRequiredMixin, ListView):
    model = Articles
    paginate_by = 20
    context_object_name = "articles"
    template_name = "articles/article_list.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ArticleList, self).get_context_data(*args, **kwargs)
        """在上下文中添加tags标签云"""
        context["popular_tags"] = Articles.objects.get_count_tags()
        return context

    def get_queryset(self):
        """获得发表的文章"""
        return Articles.objects.get_publised()


article_list_view = ArticleList.as_view()


class DraftListView(ArticleList):
    """草稿箱列表"""

    def get_queryset(self):
        """重写get_queryset方法"""
        return Articles.objects.filter(user=self.request.user).get_draft()



draft_list_view = DraftListView.as_view()


class ArticleCreateView(LoginRequiredMixin, CreateView):
    """发表文章"""
    model = Articles
    form_class = ArticleForm
    template_name = "articles/article_create.html"
    # 增加消息提示
    message = "您的文章创建成功"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        """发表文章后跳转到什么页面"""
        messages.success(self.request, self.message)  # 消息传递给下一次请求
        return reverse_lazy("articles:list")


article_create_view = ArticleCreateView.as_view()
