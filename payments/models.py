from django.db import models


CURRENCY_CHOICES = (
    ('usd','US Dollers'), 
    ('eur','Euro')
    )


class Item(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.FloatField()
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='usd')
    
    def __str__(self):
        return self.name


class Order(models.Model):
    items = models.ManyToManyField(Item)
    created_at = models.DateTimeField(null=False, auto_now=True, editable=False)
    
    def __str__(self):
        return f"#{self.id} at {str(self.created_at)}"
    
    def get_prices_sum(self):
        sum = 0
        for item in self.items.all():
            sum += item.price
            
        return sum
    
    def get_description(self):
        txt = ""
        for item in self.items.all():
            txt += f"- {item.name}\n"
        
        return txt