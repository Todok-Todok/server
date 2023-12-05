from abc import *
from django.shortcuts import get_object_or_404
from django.db.models.query import QuerySet
from django.db.models.functions import TruncMonth
from review.models import Review, UserReview, ReviewLike, ReviewScrap, ReviewComment
from django.db.models import Count

from typing import Optional,List
import random
from user.models import User
from book.models import Book

class AbstractReviewSelector(metaclass=ABCMeta):
    @abstractmethod
    def get_review_all(sort_id:int) -> "QuerySet[Review]":
        pass
    
    @abstractmethod
    def get_userreviews(user_id:int) -> "Optional[QuerySet[UserReview]]":
        pass
    
    @abstractmethod
    def get_temporary_review(user_id:int) -> "Optional[QuerySet[Review]]":
        pass
    
    @abstractmethod
    def get_review_by_review_id(review_id:int) -> Review:
        pass
    
    @abstractmethod
    def get_review_book_by_review_id(review_id:int) -> Review:
        pass
    
    @abstractmethod
    def checking_like_scrap_duplication(user_id:int,review_id:int,flag:int) -> bool:
        pass
    
    @abstractmethod
    def report_review_count_by_date(user_id:int,year:int) -> List:
        pass
    
    @abstractmethod
    def report_review_by_genre(user_id:int) -> List:
        pass
    
    @abstractmethod
    def review_like_scrap_count(review_id:int, flag:int) -> int:
        pass
    
    @abstractmethod
    def comments_by_review_id(review_id:int) -> List:
        pass
    
class ReviewSelector(AbstractReviewSelector):
    def report_review_by_genre(user_id:int) -> List:
        user = get_object_or_404(User, id=user_id)
        userreviews_objects = UserReview.objects.filter(user=user).values_list("review",flat=True).order_by('review_id')
        userreviews = Review.objects.filter(review_id__in = userreviews_objects).order_by('review_id')
        reviews = userreviews.values('genre').annotate(count=Count('*')).order_by('-count')
        return reviews
    
    def get_review_all(sort_id:int, user_id:int) -> "Optional[QuerySet[Review]]":
        if sort_id == 1:
            # 최신순으로 정렬
            reviews = Review.objects.filter(storage=True).order_by('saved_at')
            print(reviews)
            return reviews
        else:
            random_sort = random.sample(['likes','genre'], 1)
            # 추천순으로 정렬
            if random_sort == 'likes':
                # 1) 좋아요 수 많은 순서대로 정렬
                sorted_reviews = Review.objects.annotate(like_count=Count('reviewlike')).order_by('-like_count')
            else:
                genre_list = ReviewSelector.report_review_by_genre(user_id=user_id)
                sorted_reviews = []
                for item in genre_list:
                    genre = item['genre']  
                                     
                    genre_reviews = Review.objects.filter(genre=genre)
                    sorted_reviews.extend(genre_reviews)
                    
                sorted_reviews = Review.objects.filter(review_id__in=[review.review_id for review in sorted_reviews])
                return sorted_reviews
    
    def get_userreviews(user_id:int) -> "Optional[QuerySet[Review]]":
        user = get_object_or_404(User, id=user_id)
        userreview=UserReview.objects.filter(user=user).values_list("review")
        reviews = Review.objects.filter(review_id__in = userreview)
        return reviews

    def get_temporary_review(user_id:int) -> "Optional[QuerySet[Review]]":
        user = get_object_or_404(User, id=user_id)
        userreviews_objects = UserReview.objects.filter(user=user).values_list("review",flat=True).order_by('review_id')
        reviews = Review.objects.filter(review_id__in = userreviews_objects, storage=False)
        return reviews
    
    def get_review_by_review_id(review_id:int) -> Review:
        review = get_object_or_404(Review, review_id=review_id)
        return review
    
    def get_review_book_by_review_id(review_id:int) -> Review:
        review = Review.objects.select_related('book').get(review_id=review_id)
        return review
    
    def checking_like_scrap_duplication(user_id:int, review_id:int, flag:int) -> bool:
        user = get_object_or_404(User, id=user_id)
        review = ReviewSelector.get_review_book_by_review_id(review_id=review_id)
        
        if flag == 0: # ReviewLike 테이블 체크 !
            obj, created = ReviewLike.objects.get_or_create(user=user, book=review.book, review=review)
        else:
            obj, created = ReviewScrap.objects.get_or_create(user=user, book=review.book, review=review)
        return created
    
    def report_review_count_by_date(user_id:int, year:int) -> List:
        user = get_object_or_404(User, id=user_id)
        userreviews_objects = UserReview.objects.filter(user=user).values_list("review",flat=True).order_by('review_id')
        review_list = Review.objects.filter(review_id__in = userreviews_objects, saved_at__year=year).annotate(month=TruncMonth('saved_at')).values('month').annotate(count=Count('review_id')).values('month','count')
        return review_list
    
    def review_like_scrap_count(review_id:int, flag:int) -> int:
        review =  ReviewSelector.get_review_by_review_id(review_id=review_id)
        if flag == 0:
            total = ReviewLike.objects.filter(review=review).count()
        else:
            total = ReviewScrap.objects.filter(review=review).count()
        return total
        
    def comments_by_review_id(review_id:int) -> "Optional[QuerySet[ReviewComment]]":
        review = ReviewSelector.get_review_book_by_review_id(review_id=review_id)
        usercomments = ReviewComment.objects.filter(book=review.book,review=review).select_related('user')
        return usercomments
        