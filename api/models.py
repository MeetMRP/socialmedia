from django.db import models
from accounts.models import User

class Post(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    related_url = models.URLField(blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.content[:20]
    
    def total_likes(self):
        return self.likes.count()
    
class Like(models.Model):
    post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='user_likes', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('post', 'user')

class Connection(models.Model):
    STATUS_CHOICES = [
        ('accepted', 'Accepted'),
        ('pending', 'Pending'),
        ('rejected', 'Rejected'),
    ]
    
    requester = models.ForeignKey(User, related_name='requester', on_delete=models.CASCADE)
    addressee = models.ForeignKey(User, related_name='addressee', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    creation_date = models.DateTimeField(auto_now_add=True)