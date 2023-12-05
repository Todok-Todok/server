from .models import Review, ReviewComment, ReviewLike, ReviewScrap, UserReview
from django.db.models import Count
from rest_framework import serializers
from .selectors.abstracts import ReviewSelector
from user.serializers import UserSimpleSerializer
from user.models import User

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
        fields = ('title', 'content', 'category', 'genre', 'book_image',)
         
class ReviewLikeSerializer(serializers.ModelSerializer):
    like_count = serializers.SerializerMethodField(source='review')
    
    def get_like_count(self, obj):
        return ReviewSelector.review_like_scrap_count(obj.review.review_id,0)
    
    class Meta:
        model = ReviewLike
        fields = ('like_count',)

class ReviewScrapSerializer(serializers.ModelSerializer):
    scrap_count = serializers.SerializerMethodField(source='review')
    
    def get_scrap_count(self, obj):
        return ReviewSelector.review_like_scrap_count(obj.review.review_id,1)
    
    class Meta:
        model = ReviewScrap
        fields = ('scrap_count',)
        
class AllReviewCommunitySerializer(serializers.ModelSerializer):
    class Meta:
        abstract=True
        model = Review
        fields = ('title','saved_at',)
        
class SingleReviewCommentSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['user'] = UserSimpleSerializer(instance.user).data
        return response
    
    class Meta:
        model = ReviewComment
        fields = ('comment',)