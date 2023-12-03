from django.db import models
from book.models import Book
from user.models import User
# Create your models here.

class Question(models.Model):
    question_id = models.AutoField(primary_key=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True)
    content = models.TextField()
    disclosure = models.BooleanField(default=False)


    class Meta:
        managed = True
        db_table = 'Question'
        

class UserQuestion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True)
    opinion = models.TextField(default="")
    like = models.BooleanField(default=False)
    q_owner = models.BooleanField(default=False)


    class Meta:
        managed = True
        db_table = 'UserQuestion'