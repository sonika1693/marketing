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
    category = models.ForeignKey(to = Category,on_delete=models.CASCADE,null=True)
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