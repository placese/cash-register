from django.db import models


class Item(models.Model):
    """Product model in database"""
    id = models.AutoField(primary_key=True)
    title = models.CharField('Наименование товара', max_length=255)
    price = models.FloatField('Цена')

    class Meta:
        db_table = 'item'


class Receipt(models.Model):
    """Receipt model in database"""
    receipt = models.CharField(max_length=255)

    class Meta:
        db_table = 'receipt'


