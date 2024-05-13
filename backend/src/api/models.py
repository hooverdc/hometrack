from django.db import models

# Create your models here.


class Categories(models.Model):
    category_id = models.BigAutoField(primary_key=True)
    name = models.TextField(max_length=64)


class Images(models.Model):
    image_id = models.BigAutoField(primary_key=True)
    uri = models.TextField(max_length=256)


class Items(models.Model):
    item_id = models.BigAutoField(primary_key=True)
    name = models.TextField(max_length=64)
    description = models.TextField(max_length=256)
    quantity = models.IntegerField()
    # $ 99999.99
    # nobody is using 1/100 cent
    cost = models.DecimalField(max_digits=7, decimal_places=2)
    category = models.ForeignKey(Categories, on_delete=models.DO_NOTHING)
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)

    # m2m images
    images = models.ManyToManyField(Images)
