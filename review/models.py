from django.db import models
from book.models import Book
from user.models import User
# Create your models here.

class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=100)
    content = models.TextField()
    storage = models.BooleanField(default=False)
    genre = models.IntegerField() # 책 종류
    category = models.IntegerField() # 글 유형
    saved_at = models.DateTimeField()
    like_count = models.IntegerField()
    scrap_count = models.IntegerField()
    disclosure = models.BooleanField(default=False)


    class Meta:
        managed = True
        db_table = 'Review'
        
        
class ReviewLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True)
    review = models.ForeignKey(Review, on_delete=models.CASCADE, null=True)
    like = models.BooleanField(default=False)
    
    
    class Meta:
        managed = True
        db_table = 'ReviewLike'
        
        
class ReviewScrap(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True)
    review = models.ForeignKey(Review, on_delete=models.CASCADE, null=True)
    scrap = models.BooleanField(default=False)
    
    
    class Meta:
        managed = True
        db_table = 'ReviewScrap'
        
        
class ReviewComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True)
    review = models.ForeignKey(Review, on_delete=models.CASCADE, null=True)
    comment = models.TextField()
    created_at = models.DateTimeField()
    
    
    class Meta:
        managed = True
        db_table = 'ReviewComment'