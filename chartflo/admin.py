# -*- coding: utf-8 -*-

from django.contrib import admin
from .models import Chart, Number


@admin.register(Number)
class NumberAdmin(admin.ModelAdmin):
    list_display = ("legend", "slug", "updated",)
    search_fields = ("legend",)
    save_on_top = True
    readonly_fields = ('updated',)


@admin.register(Chart)
class ChartAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "updated",)
    search_fields = ("name",)
    save_on_top = True
    readonly_fields = ('updated',)
