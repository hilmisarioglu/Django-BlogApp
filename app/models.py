from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)

class Post(models.Model):
    OPTIONS = (
        ('d', 'Draft'),
        ('p', 'Published')
    )
    title = models.CharField(max_length=100)
    content = models.TextField(max_length=1000)
    image = models.ImageField()
    category = models.ForeignKey(Category , on_delete=models.PROTECT)
    #category silinse bile postlar dursun
    publish_date = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User,on_delete=models.CASCADE) #user silindiyse post da silinsin
    status = models.CharField(max_length=10, choices=OPTIONS, default='d')
    slug = models.SlugField(blank=True,unique=True)