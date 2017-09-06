# -*- coding: utf-8 -*-

from django.contrib import admin
from .models import Query, Question, Dashboard


@admin.register(Query)
class QueryAdmin(admin.ModelAdmin):
    list_display = ('name', 'app', 'model', "filters")
    search_fields = ('name',)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    filter_horizontal = ('queries',)
    save_on_top = True

    def get_readonly_fields(self, request, obj=None):
        return ("html", "script", "json")


@admin.register(Dashboard)
class DashboardAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)
    filter_horizontal = ('questions',)
    prepopulated_fields = {'slug': ('title',)}
