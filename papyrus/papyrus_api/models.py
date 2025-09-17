from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class User(User):
    # TODO: Implement user later
    pass


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=100)
    description = models.CharField(max_length=500, blank=True)
    #image = models.ImageField(upload_to='book/', blank=True)

    def __str__(self):
        return self.title
    
    def avgrating(self):
       reviews = self.reviews.all()
       if reviews.exists():
           return sum(review.rating for review in reviews) / reviews.count()

class Review(models.Model):
    book = models.ForeignKey(Book, related_name='reviews',on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='reviews',on_delete=models.CASCADE)
    rating = models.DecimalField(max_digits=3, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.book.title} ({self.rating})"
