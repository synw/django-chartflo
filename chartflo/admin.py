# -*- coding: utf-8 -*-

from django.contrib import admin
from adminsortable2.admin import SortableInlineAdminMixin
from .models import Dashboard, DashboardView


class DashboardViewInline(SortableInlineAdminMixin, admin.TabularInline):
    model = DashboardView
    fields = ["title", "slug", "active", "order"]
    prepopulated_fields = {'slug': ('title',), }
    extra = 0


@admin.register(Dashboard)
class DashboardAdmin(admin.ModelAdmin):
    list_display = ("slug", "title",)
    search_fields = ("title",)
    prepopulated_fields = {'slug': ('title',), }
    save_on_top = True
    readonly_fields = ('updated',)
    inlines = [DashboardViewInline]
