from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Item(models.Model):
    name = models.CharField(max_length=200)
    image = models.FileField()
    approved = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ['user', 'item']

    def __str__(self):
        return f'{self.item} of {self.user.last_name}'
