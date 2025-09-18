from django.contrib import admin
from papyrus_api.models import Book, Review, User
# Register your models here.

class ReviewInline(admin.TabularInline):
    model = Review

class BookAdmin(admin.ModelAdmin):
    inlines=[
        ReviewInline
    ]


admin.site.register(Book, BookAdmin)