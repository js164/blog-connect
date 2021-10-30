from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth import get_user_model

User=get_user_model()

class UserProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    photo=models.ImageField(upload_to='profile_image/',null=True)
    private_account=models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class Post(models.Model):
    author=models.ForeignKey(User, null=True,on_delete=models.CASCADE)
    title=models.CharField(max_length=256)
    text=models.TextField()
    created_date=models.DateTimeField(default=timezone.now)
    published_date=models.DateTimeField(blank=True,null=True)
    image=models.ImageField(upload_to='post_image/',null=True)

    def publish(self):
        self.published_date=timezone.now()
        self.save()

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


    def __str__(self):
        return self.text
    
    class Meta:
        ordering = ['-created_date']


class Requestsend(models.Model):
    sendby=models.ForeignKey(User,related_name='sendby',on_delete=models.CASCADE)
    sendto=models.ForeignKey(User,related_name='sendto',on_delete=models.CASCADE)
    req_confirmed=models.BooleanField(default=False)

    class Meta:
        unique_together=('sendby','sendto')

    def __str__(self):
        return self.sendby.username+"-->"+self.sendto.username

class Friends(models.Model):
    following=models.ForeignKey(User,related_name='following',on_delete=models.CASCADE)
    followers=models.ForeignKey(User,related_name='followers',on_delete=models.CASCADE)

    class Meta:
        unique_together=('following','followers')

    def __str__(self):
        return self.following.username+"-->"+self.followers.username