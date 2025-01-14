from django.db import models


class List(models.Model):
    pass


class Item(models.Model):
    text = models.TextField(default="")
    # Can we create an Item without assigning it to a list?
    list = models.ForeignKey(List, default=None, on_delete=models.CASCADE)
    # `null=True` allows the database to store `NULL` for this field.
    # `blank=True` allows the field to be empty in forms.
