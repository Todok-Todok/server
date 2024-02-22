from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import ReviewSerializer, SavedReviewSerializer, TemporaryReviewSerializer
from .services import ReviewService
from .selectors.abstracts import ReviewSelector
# Create your views here.
class ReviewCreateView(APIView):
    def post(self, request, book_id, user_id):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            ReviewService(ReviewSelector).create_review(book_id,user_id,serializer.data['review_id'])
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_206_PARTIAL_CONTENT)
    
class MyReviewView(APIView):
    def get(self, request, user_id):
        reviews = ReviewService(ReviewSelector).get_myreviews(user_id)
        return Response(reviews, status=status.HTTP_200_OK)
        
class TemporaryReviewListView(APIView):
    def get(self, request, user_id):
        reviewlist = ReviewService(ReviewSelector).get_temporary_titles(user_id)
        return Response(reviewlist, status=status.HTTP_200_OK)
    
class ReviewContentView(APIView):
    def get(self, request, review_id):
        # url parameter로 임시저장 글, 저장한 글 불러오기 구분하기
        storage_type = request.GET.get('storage', None)
        review_obj = ReviewService(ReviewSelector).get_each_review(review_id)
        if storage_type == "temporary":
            serializer = TemporaryReviewSerializer(review_obj)
        else:
            serializer = SavedReviewSerializer(review_obj)
            
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request, review_id):
        ReviewService(ReviewSelector).update_review(review_id, request.data['content'])
        return Response(status=status.HTTP_200_OK)
    
    def delete(self, request, review_id):
        review_obj = ReviewService(ReviewSelector).get_each_review(review_id)
        review_obj.delete()
        return Response(status=status.HTTP_200_OK)

# class WordCloudView(APIView):
    
class ReviewSortView(APIView):
    def get(self, request, sort_id, user_id):
        reviews = ReviewService(ReviewSelector).get_reviews(sort_id, user_id)
        return Response(reviews, status=status.HTTP_200_OK)
    
class SingleReviewAPIView(APIView):
    def get(self, request, review_id, user_id):
        review = ReviewService(ReviewSelector).get_each_community_review(review_id, user_id)
        return Response(review, status=status.HTTP_200_OK)
    
class ReviewComment(APIView):
    def post(self, request, user_id, review_id):
        ReviewService(ReviewSelector).review_comment(user_id,review_id,request.data['comment'])
        return Response(status=status.HTTP_201_CREATED) 

class ReviewLikeView(APIView):
    def post(self, request, user_id, review_id):
        created = ReviewService(ReviewSelector).review_like_scrap(user_id, review_id,0)
        if not created:
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_201_CREATED)

class ReviewScrapView(APIView):
    def post(self, request, user_id, review_id):
        created = ReviewService(ReviewSelector).review_like_scrap(user_id, review_id,1)
        if not created:
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_201_CREATED)

# 통계 페이지 관련 API
class ReviewReportView(APIView):
    def get(self, request, user_id):
        year = request.GET.get('year', None)
        result = ReviewService(ReviewSelector).review_report(user_id, year)
        return Response(result, status=status.HTTP_200_OK)
    
# 네이버 유의어 사전 크롤링
# class WordChangeView(APIView):
#     def get(self, request):
#         target_word = request.GET.get('word',None)
        
                
