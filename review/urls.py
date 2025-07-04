from django.urls import path
from . import views

urlpatterns = [
    path('<int:book_id>/<int:user_id>/',views.ReviewCreateView.as_view()),
    path('<int:user_id>/', views.MyReviewView.as_view()),
    path('temporary/<int:user_id>/', views.TemporaryReviewListView.as_view()),
    path('content/<int:review_id>/',views.ReviewContentView.as_view()),
#    path('synonym/', views.WordChangeView.as_view()),
#    path('wordcloud/', views.WordCloudView.as_view()),
    path('community/<int:user_id>/<int:sort_id>/', views.ReviewSortView.as_view()),
    path('community/detail/<int:user_id>/<int:review_id>/', views.SingleReviewAPIView.as_view()),
    path('comment/<int:user_id>/<int:review_id>/', views.ReviewComment.as_view()),
    path('like/<int:user_id>/<int:review_id>/', views.ReviewLikeView.as_view()),
    path('scrap/<int:user_id>/<int:review_id>/', views.ReviewScrapView.as_view()),
    path('report/<int:user_id>/', views.ReviewReportView.as_view()),
]