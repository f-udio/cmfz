from django.db import models

# Create your models here.


# 轮播图
class Bnner(models.Model):
    title = models.CharField(max_length=50)
    status = models.SmallIntegerField()
    create_time = models.DateField(auto_now_add=True)
    pic = models.ImageField(upload_to='pics')
