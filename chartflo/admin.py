# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Filter, Query, Question
from .charts import bar_chart
from chartflo.models import Dashboard


@admin.register(Filter)
class FilterAdmin(admin.ModelAdmin):
    list_display = ('name', "value")
    search_fields = ('name', "value")


@admin.register(Query)
class QueryAdmin(admin.ModelAdmin):
    list_display = ('name', 'app', 'model')
    search_fields = ('name',)
    filter_horizontal = ('filters',)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    filter_horizontal = ('queries',)
    save_on_top = True

    def save_model(self, request, obj, form, change):
        obj.save()
        queries = obj.queries.all()
        dataset = {}
        for q in queries:
            data = q.count_data()
            dataset[q.name] = data
        script, html = bar_chart(dataset)
        obj.html = html
        obj.script = script
        obj.save()

    def get_readonly_fields(self, request, obj=None):
        return ("html", "script")


@admin.register(Dashboard)
class DashboardAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)
    filter_horizontal = ('questions',)
    prepopulated_fields = {'slug': ('title',)}
