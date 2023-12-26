from django.db import models
from account.models import Account



class Category(models.Model):
    title = models.CharField(max_length=30)

    def __str__(self):
        return self.title


def get_product_image_filepath(self, filename):
    return 'product/product_images/' + str(self.pk) + '/product_image.png'


def get_default_product_image():
    return "product/product_default_images/default_product_image.png"

class Product(models.Model):
    title = models.CharField(max_length=30)
    desc = models.TextField()
    price = models.IntegerField(null=True,blank=True)
    quantity = models.IntegerField(null=True,blank=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    image = models.ImageField(default=get_default_product_image,upload_to=get_product_image_filepath,null=True,blank=True)

    def __str__(self):
        return self.title




class Order(models.Model):
    user = models.ForeignKey(Account,on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    payment = None
    total_price = models.IntegerField(null=True,blank=True)
    date_order = models.DateField(auto_now_add=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    tracking_code = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.product.title


class Cart(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)


class Payment(models.Model):
    user = models.ForeignKey(Account,on_delete=models.CASCADE)
    payment_number = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=100)
    amount_paid = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.payment_number








