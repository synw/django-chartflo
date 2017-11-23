# -*- coding: utf-8 -*-

from django.contrib import admin
from .models import Chart, Number, Dashboard


@admin.register(Number)
class NumberAdmin(admin.ModelAdmin):
    list_display = ("slug", "generator", "modelnames", "legend", "updated")
    save_on_top = True
    readonly_fields = ('updated',)


@admin.register(Chart)
class ChartAdmin(admin.ModelAdmin):
    list_display = ("slug", "generator", "modelnames", "updated")
    save_on_top = True
    readonly_fields = ('updated',)


@admin.register(Dashboard)
class DashboardAdmin(admin.ModelAdmin):
    list_display = ("slug", "title",)
    search_fields = ("title",)
    prepopulated_fields = {'slug': ('title',), }
    save_on_top = True
    readonly_fields = ('updated',)
