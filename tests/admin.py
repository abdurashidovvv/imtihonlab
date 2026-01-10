from django.contrib import admin
from django.utils.html import format_html
from .models import Test

@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ("title", "created_by", "created_at", "test_file_link", "answer_file_link")
    list_filter = ("created_by", "created_at")
    search_fields = ("title", "description")
    readonly_fields = ("test_file_link", "answer_file_link")

    def test_file_link(self, obj):
        if obj.test_file:
            return format_html('<a href="{}" target="_blank">PDF Question</a>', obj.test_file.url)
        return "-"
    test_file_link.short_description = "Test File"

    def answer_file_link(self, obj):
        if obj.answer_file:
            return format_html('<a href="{}" target="_blank">PDF Answer</a>', obj.answer_file.url)
        return "-"
    answer_file_link.short_description = "Answer File"
