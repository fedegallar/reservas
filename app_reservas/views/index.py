# coding=utf-8

from django.views.generic.base import TemplateView


class IndexView(TemplateView):
    template_name = 'app_reservas/index.html'
