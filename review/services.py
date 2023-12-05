from .selectors.abstracts import ReviewSelector
from typing import List, Optional, Dict
from .serializers import ReviewSerializer, ReviewListSerializer, ReviewTitleSerializer, AllReviewCommunitySerializer, SingleReviewCommentSerializer
from .models import Review, ReviewComment, UserReview
from django.shortcuts import get_object_or_404
from user.serializers import UserSimpleSerializer

from user.models import User
from book.models import Book

@staticmethod
def review_format(self, review:Review, user:User):
    review_serializer = AllReviewCommunitySerializer(review)
    review_serializer=review_serializer.data
    user_serializer = UserSimpleSerializer(user)
    review_serializer.update(user_serializer.data)
    review_serializer.update({"like_count":self.selector.review_like_scrap_count(review.review_id,0),"scrap_count":self.selector.review_like_scrap_count(review.review_id,1)})
    return review_serializer
    
class ReviewService:
    def __init__(self, selector: ReviewSelector):
        self.selector = selector
    
    def create_review(self, book_id: int, user_id:int, review_id:int) -> None:
        book=get_object_or_404(Book,book_id=book_id)
        review = self.selector.get_review_by_review_id(review_id=review_id)
        review.book=book
        review.save()
        user=get_object_or_404(User,id=user_id)
        UserReview.objects.create(book=book,review=review,user=user)
        return None
        
    def get_reviews(self, sort_id:int, user_id:int) -> List:
        reviews = self.selector.get_review_all(sort_id=sort_id, user_id=user_id)
        # 하드 코딩
        user = get_object_or_404(User,id=user_id)
        responsebody=[]
        for review in reviews:
            review_serializer = review_format(self, review, user_id)
            responsebody.append(review_serializer)
        return responsebody
        
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
    
    def get_each_community_review(self, review_id:int, user_id:int) -> List:
        review = self.selector.get_review_by_review_id(review_id=review_id)
        # 하드코딩
        user = get_object_or_404(User,id=user_id)
        review_serializer = review_format(self, review, user)
        usercomments=self.selector.comments_by_review_id(review_id)
        comment_serializer=SingleReviewCommentSerializer(usercomments,many=True)
        review_serializer.update({"comments":comment_serializer.data})
        return review_serializer
    
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