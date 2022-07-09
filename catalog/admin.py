from django.contrib import admin
from django.contrib.admin import ModelAdmin, TabularInline

from .models import *


class BookInstanceInline(TabularInline):
    model = BookInstance


@admin.register(Book)
class BookAdmin(ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    inlines = [BookInstanceInline]


@admin.register(Author)
class AuthorAdmin(ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]


@admin.register(Genre)
class GenreAdmin(ModelAdmin):
    pass


@admin.register(BookInstance)
class BookInstanceAdmin(ModelAdmin):
    list_filter = ('status', 'due_back')
    list_display = ('book', 'status', 'borrower', 'due_back', 'id')
    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back', 'borrower')
        }),
    )
