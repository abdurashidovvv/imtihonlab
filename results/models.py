from django.db import models
from django.conf import settings
from tests.models import Test


class Result(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # 👈 MUHIM
        on_delete=models.CASCADE,
        related_name='results'
    )
    test = models.ForeignKey(
        Test,
        on_delete=models.CASCADE,
        related_name='results'
    )
    score = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'test')

    def __str__(self):
        return f"{self.user} - {self.test.title}"
