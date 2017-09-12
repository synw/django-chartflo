# -*- coding: utf-8 -*-

from django.contrib import admin
from .models import Chart, Number


@admin.register(Number)
class NumberAdmin(admin.ModelAdmin):
    list_display = ("name", "slug",)
    search_fields = ("name",)
    save_on_top = True


@admin.register(Chart)
class ChartAdmin(admin.ModelAdmin):
    list_display = ("name", "slug",)
    search_fields = ("name",)
    save_on_top = True
