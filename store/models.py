from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth import get_user_model

User = get_user_model()
rating_choice = (
    (1,'1 star'),
    (1.5,'1.5 star'),
    (2,'2 star'),
    (2.5,'2.5 star'),
    (3,'3 star'),
    (3.5,'3.5 star'),
    (4,'4 star'),
    (4.5,'4.5 star'),
    (5,'5 star'),
)
class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True
        ordering = ['-updated_at','-created_at']

class Category(models.Model):
    name = models.CharField(max_length=255),
    slug = models.SlugField(max_length=255,unique=True)
    image = models.ImageField(upload_to = 'Category/')

    class Meta:
        verbose_name = "category"
        verbose_name_plural = 'categories'

    def save(self,*args,**kwargs):
        if not self.id:
            super().save(*args,**kwargs)

        if not self.slug:
            self.slug = slugify(name)
        super().save(*args,**kwargs)


class Product(TimeStampModel):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="user_item")
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name = 'products')
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255,unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10,decimal_places=2)
    stock_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name
    
class ProductImage(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name="productimage")
    image = models.ImageField(upload_to='ProductImage/')

    def __str__(self):
        return self.product.name

class Variation(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name="product_variation")
    size = models.CharField(max_length=100,blank=True)
    color = models.CharField(max_length=100,blank=True)

    def __str__(self):
        return f"{self.product}-{self.size}-{self.color}"

class ProductReview(TimeStampModel):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="product_review_user")
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name="product_review")
    comment = models.TextField()
    rating = models.PositiveIntegerField(choices = rating_choice)

    def __str__(self):
        return self.product.name

