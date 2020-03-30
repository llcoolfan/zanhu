#!/usr/bin/python3
# -*- coding=utf-8 -*-
# Author:llcoolf

from django import forms
from article.models import Articles


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Articles
        fields = ["title", "content", "image", "tags"]
