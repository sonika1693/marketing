from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50,null=True,blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

class Content(models.Model):
    category = models.ForeignKey(to = Category,on_delete=models.PROTECT,null=True)
    title = models.CharField(max_length=300,null=True,blank=True)
    description = models.TextField(null=True, blank=True)
    media_type_choices = [
        ('image', 'image'),
        ('video', 'video'),
    ]
    media_type = models.CharField(max_length=100, choices=media_type_choices, null=True, blank=True)
    image_url = models.CharField(max_length=300,null=True,blank=True)
    video_url = models.CharField(max_length=300,null=True,blank=True)
    price = models.FloatField(default=0)
    is_locked = models.BooleanField(default=False)
    home = models.BooleanField(default=False)
    date = models.DateField(auto_now=True)

    def __str__(self):
        return self.title
    
class ContentComments(models.Model):
    user = models.ForeignKey(to = User,on_delete=models.CASCADE,null=True)
    content = models.ForeignKey(to = Content,on_delete=models.CASCADE,null=True)
    comment = models.TextField(null=True,blank=True)
    date = models.DateField(auto_now=True)

    def __str__(self):
        return self.content.title
    
    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
    
class ContentLikes(models.Model):
    user = models.ForeignKey(to = User,on_delete=models.CASCADE,null=True)
    content = models.ForeignKey(to = Content,on_delete=models.CASCADE,null=True)
    likes = models.BooleanField(default=False)
    date = models.DateField(auto_now=True) # when update valuse will be updated

    def __str__(self):
        return self.content.title
    
    class Meta:
        verbose_name = "Like"
        verbose_name_plural = "Likes"

class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    content = models.ForeignKey(Content,on_delete=models.CASCADE,null=True,blank=True)
    date = models.DateField(auto_now_add=True,null=True,blank=True)

class Payment(models.Model):
    txn_id = models.CharField(max_length=100) # Transaction id
    payment_method = models.CharField(max_length=100)
    amount_paid = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.txn_id


class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.PROTECT,null=True,blank=True)
    payment = models.ForeignKey(Payment, on_delete=models.PROTECT,blank=True, null=True)
    order_number = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=100)
    total_amount = models.FloatField()
    STATUS = (
        ('New','New'),
        ('Accepted','Accepted'),
        ('Completed','Completed'),
        ('Cancelled','Cancelled'),
    )
    status = models.CharField(max_length=10, choices=STATUS,default='New')
    ip = models.CharField(max_length=20,blank=True)
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class OrderContent(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    content = models.ForeignKey(Content,on_delete=models.PROTECT)
    ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

