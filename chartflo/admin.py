# -*- coding: utf-8 -*-

from django.contrib import admin
from .models import Dashboard


@admin.register(Dashboard)
class DashboardAdmin(admin.ModelAdmin):
    list_display = ("slug", "title",)
    search_fields = ("title",)
    prepopulated_fields = {'slug': ('title',), }
    save_on_top = True
    readonly_fields = ('updated',)
