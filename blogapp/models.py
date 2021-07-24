from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth import get_user_model

User=get_user_model()

# Create your models here.
class Post(models.Model):
    author=models.ForeignKey(User, null=True,on_delete=models.CASCADE)
    title=models.CharField(max_length=256)
    text=models.TextField()
    created_date=models.DateTimeField(default=timezone.now)
    published_date=models.DateTimeField(blank=True,null=True)
    image=models.ImageField(upload_to='post_image/',null=True)
    # likes=models.ManyToManyField(User,related_name='post_likes')

    def publish(self):
        self.published_date=timezone.now()
        self.save()

    def approve_comment(self):
        return self.comments.filter(approve_comment=True)

    def get_absolute_url(self):
        return reverse("post_detail",kwargs={'pk':self.pk})

    def __str__(self):
        return self.title

class PostLike(models.Model):
    post = models.ForeignKey(Post,related_name='post_likes',on_delete=models.CASCADE)
    like_by=models.ForeignKey(User,on_delete=models.PROTECT)

    class Meta:
        unique_together = ('post', 'like_by',)
    
    def __str__(self):
        return self.post.title+"--"+self.like_by.username


class Comment(models.Model):
    post=models.ForeignKey('blogapp.Post',related_name='comments',on_delete=models.CASCADE)
    author=models.CharField(max_length=256)
    text=models.TextField()
    created_date=models.DateTimeField(default=timezone.now)

    def get_absolute_url(self):
        return reverse("post_list")

    def __str__(self):
        return self.text
    
    class Meta:
        ordering = ['-created_date']
