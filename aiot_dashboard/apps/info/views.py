# coding: utf-8

from django.views.generic.base import TemplateView

class InfoView(TemplateView):
    template_name = "info/info.html"
