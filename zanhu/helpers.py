#!/usr/bin/python3
# -*- coding=utf-8 -*-
# Author:llcoolf
from functools import wraps
from django.http import HttpResponseBadRequest
from django.views.generic import View
from django.core.exceptions import PermissionDenied


def ajax_required(f):
    @wraps(f)
    def wrapper(request, *args, **kwargs):
        """是否为ajax请求"""
        if not request.is_ajax():
            return HttpResponseBadRequest("不是AJAX请求")
        return f(request, *args, **kwargs)

    return wrapper


class AuthorRequiredMixin(View):
    """
    验证是否为原作者，用于文章删除，文章编辑
    """

    def dispatch(self, request, *args, **kwargs):
        # 状态和文章都含有user属性
        if self.get_object().user.username != self.request.user.username:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
