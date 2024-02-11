from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Post(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()

    def __str__(self):
        return self.title

class Rating(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])

    class Meta:
        unique_together = ('post', 'user')

    def __str__(self):
        return f"{self.user.username}: {self.score}"