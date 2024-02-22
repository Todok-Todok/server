from django.urls import path
from . import views

urlpatterns = [
    path('<int:book_id>/<int:user_id>/', views.QuestionCreateView.as_view()),
    path('share/<int:question_id>/', views.QuestionShareView.as_view()),
#     path('<int:book_id>/create/', ),   # ai model 연결한 후, 구현할 예정
    path('receive/<int:book_id>/<int:user_id>/', views.QuestionReceiveView.as_view()),
    path('save/<int:question_id>/<int:user_id>/', views.QuestionSaveView.as_view()),
    path('detail/<int:user_id>/<int:question_id>/', views.QuestionContentView.as_view()),
    path('detail/reaction/<int:question_id>/', views.SharedQuestionReactionView.as_view()),
]
