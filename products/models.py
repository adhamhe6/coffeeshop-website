from django.db import models
from django.utils import timezone

FLAG_OPTION = (
    ('Hot Coffee', 'Hot Coffee'),
    ('Cold Coffee', 'Cold Coffee'),
)

class Product(models.Model):
    name = models.CharField(max_length=120)
    desc = models.TextField(max_length=10000)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='products/images/')
    is_active = models.BooleanField(default=True)
    publish_date = models.DateTimeField(default=timezone.now)
    flag = models.CharField(max_length=20, choices=FLAG_OPTION)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-publish_date']