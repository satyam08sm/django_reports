from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='products', default='no_picture.png')
    price = models.FloatField(help_text='in INR')
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name} - {self.created_date.strftime("%d/%m/%Y")}'
