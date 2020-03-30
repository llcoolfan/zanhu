from django.db import models
from django.conf import settings
from slugify import slugify
from taggit.managers import TaggableManager


class ArticleQureySet(models.query.QuerySet):
    """自定义QuerySet，提高模型类的可用性"""

    def get_publised(self):
        """返回已经发表的文章"""
        return self.filter(status="P")

    def get_draft(self):
        """返回草稿"""
        return self.filter(status="D")

    def get_count_tags(self):
        """统计所有发表文章的所有标签"""
        tag_dict = {}
        for obj in self.all():
            for tag in obj.tags.names():
                if tag not in tag_dict:
                    tag_dict[tag] = 1
                else:
                    tag_dict[tag] += 1
        return tag_dict.items()


class Articles(models.Model):
    STATUS = (("D", "Draft"), ("P", "Publised"))  # 两个元祖
    title = models.CharField(max_length=255, unique=True, verbose_name="标题")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL,
                             related_name="author", verbose_name="作者")
    image = models.ImageField(upload_to="articles_image/%Y/%m/%d/", verbose_name="文章图片")
    slug = models.SlugField(max_length=255, verbose_name="URL别名")
    tags = TaggableManager(help_text="多个标签使用,（英文）隔开", verbose_name="标签")
    status = models.CharField(max_length=1, choices=STATUS, default="D", verbose_name="状态")
    content = models.TextField(verbose_name="内容")
    edited = models.BooleanField(default=False, verbose_name="是否可以编辑")
    create_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    objects = ArticleQureySet.as_manager()

    class Meta:
        verbose_name = "文章"
        verbose_name_plural = verbose_name
        ordering = ("-create_at",)

    def __str__(self):
        return self.title

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        """重写save方法，每次保存时，生成slug"""
        self.slug = slugify(self.title)
        super(Articles, self).save()
