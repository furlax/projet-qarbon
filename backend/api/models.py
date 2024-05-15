from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.core.validators import MinValueValidator, MaxValueValidator


class Message(models.Model):
    subject = models.CharField(max_length=200)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Place(models.Model):
    name = models.CharField(max_length=80)
    street = models.CharField(max_length=200)
    number = models.IntegerField()
    postal_code = models.IntegerField()
    locality = models.CharField(max_length=200)
    image = models.ImageField(upload_to='places/images/', null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # img = Image.open(self.image.path)

        # if img.height > 500 or img.width > 500:
        #     output_size = (500, 500)
        #     img.thumbnail(output_size)
        #     img.save(self.image.path)

    def average_rating(self):
        avg_rating = self.rating_set.all().aggregate(models.Avg('rating')).get('rating__avg')
        if avg_rating is None:
            return "No ratings yet"
        else:
            return round(avg_rating, 2)

    def __str__(self):
        return self.name
    
class Event(models.Model):
    name = models.CharField(max_length=80)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=6)
    date = models.DateTimeField(auto_now=False, auto_now_add=False)
    image = models.ImageField(upload_to='events/images/', null=True, blank=True)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events')
    participants = models.ManyToManyField(User, related_name='participating_events', blank=True)
    capacity = models.IntegerField(default=0)

    def is_full(self):
        return self.participants.count() >= self.capacity

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 500 or img.width > 500:
            output_size = (500, 500)
            img.thumbnail(output_size)
            img.save(self.image.path)

    def __str__(self):
        return self.name 

class Comment(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='comments', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)

class Rating(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='ratings')
    rated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings_given')
    rating = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(5)])

    def __str__(self):
        return f'{self.rated_by.username} rated {self.place.name} {self.rating}'
    

class Waitlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

class MessagesUsers(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    sender_deleted = models.BooleanField(default=False)
    receiver_deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f'{self.sender.username} to {self.receiver.username}'