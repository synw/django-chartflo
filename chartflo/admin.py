# -*- coding: utf-8 -*-

from django.contrib import admin
from .models import Query, Question, Dashboard, Chart, Number


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


@admin.register(Query)
class QueryAdmin(admin.ModelAdmin):
    list_display = ("name", "app", "model", "filters")
    search_fields = ("name",)
    save_on_top = True


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    filter_horizontal = ("queries",)
    save_on_top = True


@admin.register(Dashboard)
class DashboardAdmin(admin.ModelAdmin):
    list_display = ("title",)
    search_fields = ("title",)
    filter_horizontal = ("questions", "charts")
    prepopulated_fields = {"slug": ("title",)}
    save_on_top = True
