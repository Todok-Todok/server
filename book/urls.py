from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.SearchAPIView.as_view()),
    path('<int:user_id>/<int:book_id>/', views.BookAllAPIView.as_view()),
    path('booklist/<int:user_id>/', views.BookTitleAPIView.as_view()),
    path('add/<int:b_status>/<int:user_id>/',views.AddUserBookAPIView.as_view()),
]