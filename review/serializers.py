from .models import Review, ReviewComment, ReviewLike, ReviewScrap
from django.db.models import Count
from rest_framework import serializers
from user.serializers import UserSimpleSerializer
from .selectors.abstracts import ReviewSelector

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
         
         
         
class AllReviewCommunitySerializer(serializers.ModelSerializer):
    like_count = serializers.SerializerMethodField()
    scrap_count = serializers.SerializerMethodField()
    
    def __init__(self, selector: ReviewSelector):
        self.selector = selector
            
    def get_like_count(self, obj):
        return self.selector.review_like_scrap_count(obj.review_id,0)

    def get_scrap_count(self, obj):
        return self.selector.review_like_scrap_count(obj.review_id,1)
    
    def get_user(self, obj):
        return UserSimpleSerializer(self.selector.get_user_by_review_id(obj.review_id)).data

    class Meta:
        abstract = True
        model = Review
        fields = ('title','saved_at','like_count','scrap_count','user',)
        
class SingleReviewCommentSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['user'] = UserSimpleSerializer(instance.user).data
        return response
    
    class Meta:
        model = ReviewComment
        fields = ('content',)

class SingleReviewCommunitySerializer(AllReviewCommunitySerializer):
    reviewcomment_set = SingleReviewCommentSerializer(many=True, read_only=True)
    
    class Meta:
        fields = ('title','saved_at','like_count','scrap_count','reviewcomment_set',)