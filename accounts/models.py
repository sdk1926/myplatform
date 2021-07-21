from django.db import models

# Create your models here.

class Accounts(models.Model):
    user_id = models.CharField(
        max_length=128,
        unique=True,
    )
    email = models.EmailField(
        max_length=128,
        null=True,
    )
    password = models.CharField(
        max_length=2048,
    )
    created = models.DateTimeField(
        auto_now_add=True
        )
    class Meta:
        verbose_name = '계정'
        verbose_name_plural = '계정'
        ordering = ['-created', ]

    def __str__(self):
        return self.user_id

