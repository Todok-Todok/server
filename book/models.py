from django.db import models
from user.models import User
# Create your models here.

class Book(models.Model):
    book_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    book_image = models.CharField(max_length=256, blank=True, default="")
    author = models.CharField(max_length=50)
    publisher = models.CharField(max_length=50)
    
    
    class Meta:
        managed = True
        db_table = 'Book'
    
    
class UserBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True)
    status = models.IntegerField()       # 1 : 읽고 있는 책 (now), 2 : 읽은 책 (done), 3 : 읽고 싶은 책 (wish)


    class Meta:
        managed = True
        db_table = 'UserBook'