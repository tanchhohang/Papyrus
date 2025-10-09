import uuid
from django.db import models
from django.db.models import Avg
from django.contrib.auth.models import User

#TODO use of UUID inetead of default id
# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=100)
    description = models.CharField(max_length=500, blank=True)
    #image = models.ImageField(upload_to='book/', blank=True)

    def __str__(self):
        return self.title
    
    def avgrating(self):
        avg = self.reviews.aggregate(Avg('rating'))['rating__avg']
        return round(avg,1)

class Review(models.Model):
    book = models.ForeignKey(Book, related_name='reviews',on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='reviews',on_delete=models.CASCADE)
    rating = models.DecimalField(max_digits=3, decimal_places=1)
    comment = models.CharField(max_length=500, blank=True, default='Good Book')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.book.title} ({self.rating})"
