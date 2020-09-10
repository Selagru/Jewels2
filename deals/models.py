from django.db import models
from django.utils import timezone
from items.models import Item
from django.contrib.auth.models import User


class Deal(models.Model):
    customer = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    total = models.PositiveSmallIntegerField(help_text='Сумма сделки:')
    quantity = models.PositiveSmallIntegerField(default=1, help_text='Количество товара (шт):')
    date = models.DateTimeField(default=timezone.now, null=True, blank=True,
                                help_text='Дата и время регистрации сделки:')

    class Meta:
        ordering = ['customer']

    def __str__(self):
        return f'{self.customer} {self.date}'
