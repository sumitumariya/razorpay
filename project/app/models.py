from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
class ItemInfo(models.Model):
    iten_name = models.CharField(max_length=200)
    item_desc = models.CharField(max_length=200)
    item_price = models.IntegerField()
    item_image = models.ImageField(upload_to="image")

class Product(models.Model):
    amount = models.CharField(max_length=100 , blank=True)
    order_id = models.CharField(max_length=1000 )
    razorpay_payment_id = models.CharField(max_length=1000 ,blank=True)
    paid = models.BooleanField(default=False)
    def __str__(self):
        return self.name