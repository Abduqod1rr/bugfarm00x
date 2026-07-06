from django.db import models
from django.contrib.auth.models import User


class Poc(models.Model):
    title=models.CharField(max_length=20,default='no title')
    content=models.FileField(upload_to='picpokcontent', blank=True, default='picpokcontent/Google Dino Online.jpeg')
    owner=models.ForeignKey(User,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    like=models.ManyToManyField(User,related_name='liked_poc')

    def __str__(self):
        return self.title
    

class Comment(models.Model):
    poc=models.ForeignKey(Poc, on_delete=models.CASCADE)
    text=models.TextField()
    coment_owner=models.ForeignKey(User, on_delete=models.CASCADE)
    comented_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text
    

class Profile(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    bio=models.CharField(max_length=50,default='nothing')
    picture=models.ImageField(default='profile_pictures/Google Dino Online.jpeg',upload_to='profile_pictures')
 
    class Meta:
        unique_together = ('user',)
        
    def __str__(self):
        return self.user


class BugProgress(models.Model):
    BUG_CHOICES = [
        ('sqli', 'SQL Injection'),
        ('xss', 'Reflected XSS'),
        ('idor', 'IDOR'),
        ('file_upload', 'Unrestricted File Upload'),
        ('open_redirect', 'Open Redirect'),
        ('info_disclosure', 'Information Disclosure'),
        ('weak_crypto', 'Weak Password Storage'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bug_id = models.CharField(max_length=20, choices=BUG_CHOICES)
    found_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'bug_id')

    def __str__(self):
        return f"{self.user.username} found {self.get_bug_id_display()}"