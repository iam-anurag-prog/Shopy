from django.db import models

# Create your models here.
class Product(models.Model):
    product_id =models.AutoField
    product_name = models.CharField(max_length=50)
    category = models.CharField(max_length=50, default="")
    subcategory = models.CharField(max_length=50, default="")
    price = models.IntegerField(default=0)
    product_desc = models.CharField(max_length=2500)
    product_desc2 = models.CharField(max_length=2500, default="")
    image = models.ImageField(upload_to="shopy/images", default="")

    def __str__(self):
        return self.product_name

class Contact(models.Model):
    msg_id =models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50, default="")
    phone = models.CharField(max_length=50, default="")
    desc = models.CharField(max_length=500, default="")

    def __str__(self):
        return self.name

class Order(models.Model):
    order_id =models.AutoField(primary_key=True)
    ItemJson =models.CharField(max_length=500, default='')
    amount = models.IntegerField(default=0)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50, unique=True)
    address = models.CharField(max_length=100)
    address2 = models.CharField(max_length=100)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=30)
    zip_code = models.CharField(max_length=10)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return f"Order {self.order_id}"

class OrderUpdate(models.Model):
    update_id = models.AutoField(primary_key=True)
    order_id = models.IntegerField(default="")
    update_desc = models.CharField(max_length=500)
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.update_desc[0:7] + "... "


