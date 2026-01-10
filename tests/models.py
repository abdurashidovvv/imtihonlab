from django.db import models
from django.conf import settings


class Test(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    test_file = models.FileField(upload_to="tests/pdfs/")
    answer_file = models.FileField(upload_to="tests/answers/")

    open_questions_count = models.PositiveIntegerField(default=35)
    closed_questions_count = models.PositiveIntegerField(default=10)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_tests"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
