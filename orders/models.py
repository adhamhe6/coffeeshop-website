from django.db import models
from django.contrib.auth.models import User
from products.models import Product
from creditcards.models import CardNumberField, CardExpiryField, SecurityCodeField

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    details = models.ManyToManyField(Product, through='OrderDetails')
    order_date = models.DateTimeField()
    is_finished = models.BooleanField()
    total = 0
    items_count = 0
    
    def __str__(self):
        return 'User: ' + self.user.username + ', Order Id: ' + str(self.id)
class OrderDetails(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    quantity = models.IntegerField()
    
    def __str__(self):
        return 'User: ' + self.order.user.username + ', Product: ' + self.product.name + ', Order Id: ' + str(self.order.id)

    class Meta:
        ordering = ['-id']
class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    shipment_address = models.CharField(max_length=150)
    shipment_phone = models.CharField(max_length=50)
    card_number = CardNumberField(verbose_name = "Card Number")
    expire = CardExpiryField(verbose_name = "Expiration Date")
    security_code = SecurityCodeField(verbose_name = "Security Code")