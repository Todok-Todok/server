from .selectors.abstracts import ReviewSelector
from typing import List, Optional, Dict
from .serializers import ReviewSerializer, ReviewListSerializer, ReviewTitleSerializer
from .models import Review, ReviewComment, ReviewLike, ReviewScrap
from django.shortcuts import get_object_or_404

from user.models import User

class ReviewService:
    def __init__(self, selector: ReviewSelector):
        self.selector = selector
        
    def get_reviews(self, sort_id:int, user_id:int) -> List:
        reviews = self.selector.get_review_all(sort_id=sort_id, user_id=user_id)
        serializer = ReviewSerializer(reviews, many=True)
        return serializer.data
    
    def get_myreviews(self, user_id:int) -> List:
        myreviews = self.selector.get_userreviews(user_id=user_id)
        serializer = ReviewListSerializer(myreviews, many=True)
        return serializer.data
    
    def get_temporary_titles(self, user_id:int) -> List:
        reviews = self.selector.get_temporary_review(user_id=user_id)
        serializer = ReviewTitleSerializer(reviews, many=True)
        return serializer.data
    
    def get_each_review(self, review_id:int) -> Review:
        review = self.selector.get_review_by_review_id(review_id=review_id)
        return review
    
    def update_review(self, review_id:int, content: Optional[str]) -> None:
        review = self.selector.get_review_by_review_id(review_id=review_id)
        review.content = content
        review.save()
        return None
    
    def review_comment(self, user_id:int, review_id:int, comment: str) -> None:
        user=get_object_or_404(User, id=user_id)
        review = self.selector.get_review_book_by_review_id(review_id=review_id)
        ReviewComment.objects.create(user=user,book=review.book,review=review,comment=comment)
        return None
    
    def review_like_scrap(self, user_id:int, review_id:int, flag:int) -> None:
        # like 표시하기
        if flag == 0:
            created = self.selector.checking_like_scrap_duplication(user_id=user_id, review_id=review_id,flag=0)
        # scrap 하기
        else:
            created = self.selector.checking_like_scrap_duplication(user_id=user_id, review_id=review_id,flag=1)
        if not created:
            raise ValueError("이미 좋아요 또는 스크랩 표시를 했습니다 !")
        return None
    
    def review_report(self, user_id:int, year:int) -> Dict[str, List]:
        by_genre = self.selector.report_review_by_genre(user_id=user_id)
        by_date = self.selector.report_review_count_by_date(user_id=user_id, year=year)
        responsebody={"by_genre":by_genre,"by_date":by_date}
        return responsebody