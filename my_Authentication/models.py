from django.db import models

# Create your models here.
class user_login(models.Model):
    username = models.CharField(max_length=100,verbose_name="用户名")
    password = models.CharField(max_length=100,verbose_name="密码")
    token=models.CharField(max_length=100,verbose_name="token",blank=True,null=True)
    def __str__(self):
        return self.username
