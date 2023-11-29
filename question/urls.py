from django.urls import path
from . import views

urlpatterns = [
    path('<int:book_id>/<int:user_id>/', views.QuestionCreateView.as_view()),
#    path('<int:book_id>/share/', views.QuestionShareView.as_view()),
#     path('<int:book_id>/create/', ),
#     path('<int:book_id>/receive/', ),
#     path('<int:book_id>/detail/<int:question_id>/'),
#     path('<int:book_id>/detail/<int:question_id>/reaction/'),
]