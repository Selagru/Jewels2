from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=100, help_text='Название камня:')
    cost = models.IntegerField(default=500, help_text='Цена:')
    file = models.FileField

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
