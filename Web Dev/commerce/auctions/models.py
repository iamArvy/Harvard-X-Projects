from django.contrib.auth.models import AbstractUser
from django.db import models

class Categories(models.Model):
    name = models.CharField(max_length=60)
    img = models.URLField( blank=True, null=True )
    def __str__(self):
        return f"{self.name}"
    
class User(AbstractUser):
    email = models.EmailField(unique=True)
    watchlist = models.ManyToManyField('Listings', related_name='watchlist', blank=True)
    auctions = models.ManyToManyField('Listings', related_name='auctions', blank=True)

    def __str__(self):
        return self.username

class Listings(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=60)
    desc = models.TextField(max_length=120, null=True, blank=True)
    img = models.URLField(null=True, blank=True)
    cat = models.ForeignKey(Categories, null=True, on_delete=models.CASCADE, blank=True)
    startprice = models.IntegerField(default=0)
    highestbid = models.ForeignKey('Bids', null=True, blank=True, on_delete=models.DO_NOTHING)
    created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.title} by {self.user.username}"
    
class Bids(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    list = models.ForeignKey(Listings, on_delete=models.CASCADE)
    amount = models.CharField(max_length=20)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'list')

    def __str__(self):
        return f"Bid by {self.user.username} on {self.list.title}"
    

class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    clist = models.ForeignKey(Listings, on_delete=models.CASCADE)
    comments = models.TextField(max_length=300)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.comments} by {self.user.username} on {self.clist.title} Listing"
# python manage.py migrate
