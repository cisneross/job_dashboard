from django.db import models
# Create your models here.
# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at =models.DateTimeField(auto_now=True)

class Jobs (models.Model):
    name = models.CharField(max_length=200)
    desc = models.TextField()
    location = models.CharField(max_length=200)
    juploader = models.ForeignKey(User,related_name="uploaded_jobs",on_delete=models.CASCADE)
    my_jobs = models.ForeignKey(User,related_name="all_jobs",on_delete=models.CASCADE,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at =models.DateTimeField(auto_now=True)