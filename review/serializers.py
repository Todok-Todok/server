from .models import Review, ReviewComment, ReviewLike, ReviewScrap
from rest_framework import serializers

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
        
class ReviewListSerializer(serializers.ModelSerializer):
    book_image = serializers.SerializerMethodField()
    
    def get_book_image(self, obj):
        return obj.book.book_image
    
    class Meta:
        model = Review
        fields = ('review_id','title','category','saved_at','disclosure','book_image',)
        
class ReviewTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('review_id','title',)

class TemporaryReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('title','content','genre','category','disclosure',)
        
class SavedReviewSerializer(serializers.ModelSerializer):
    book_image = serializers.SerializerMethodField()
    
    def get_book_image(self, obj):
        return obj.book.book_image
    
    class Meta:
        model = Review
        fields = ('titie', 'content', 'category', 'genre', 'book_image',)